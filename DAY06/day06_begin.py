import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AgentDefinition,
    AssistantMessage,
    ToolUseBlock,
    ResultMessage,
)

# The system-level contract. The entire five-agent run must produce
# this structure, or the run fails loudly instead of shipping prose.
REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "executive_summary": {"type": "string"},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "claim": {"type": "string"},
                    "citations": {"type": "array", "items": {"type": "integer"}},
                },
                "required": ["claim", "citations"],
            },
        },
        "conflicts": {"type": "array", "items": {"type": "string"}},
        "limitations": {"type": "string"},
        "references": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "url": {"type": "string"},
                    "date": {"type": "string"},
                },
                "required": ["id", "title", "url"],
            },
        },
    },
    "required": ["title", "executive_summary", "findings", "references"],
}

SEARCH_AGENT = AgentDefinition(
    description=(
        "Searches the web for credible sources on one specific topic. "
        "Use whenever a task requires finding new information."
    ),
    prompt="""You are a research search agent.
              Search the web for the topic you are given.
              Find at least five distinct, credible sources.
              For each source report the title, URL, publication date if available,
              and a two-sentence summary.
              Do not analyze or draw conclusions. Just search and report. If you cannot search, 
              report that you could not search and stop. Do not attempt workarounds.""",
    tools=["WebSearch"],
    maxTurns=10,
)

ANALYSIS_AGENT = AgentDefinition(
    description=(
        "Analyzes ONE set of sources on ONE topic and extracts key "
        "findings. Use once per search result set. Cannot search the web."
    ),
    prompt="""You are a research analysis agent.
              You receive sources found by a search agent on a single topic.
              Extract the key findings:
              - The main claims, each tagged with the title AND URL of every
                source that supports it
              - Points where sources disagree, with each position attributed
                by title and URL
              - Gaps the sources do not cover
              Be complete but compact: every claim, disagreement, and gap
              survives, but no filler prose. Your output shares a context
              window with every other analysis downstream.
              Never mention a claim without its source URLs.
              Do not resolve disagreements. Do not search the web.""",
    tools=[],
    maxTurns=5,
)

SYNTHESIS_AGENT = AgentDefinition(
    description=(
        "Combines multiple analyses into one unified picture and "
        "resolves conflicts between them. Use exactly once, after all "
        "analyses are complete. Cannot search the web."
    ),
    prompt="""You are a research synthesis agent.
          You receive analyses of several topics, each containing claims,
          disagreements, and gaps, all with source URLs attached.
          Produce one unified synthesis:

          1. State the overall picture that emerges across all analyses.
          2. For every conflict between sources, resolve it explicitly:
            - Prefer claims corroborated by multiple independent sources.
            - Prefer more recent sources when facts change over time.
            - Prefer primary sources over secondary reporting.
            - If the conflict cannot be resolved, say so and present
              both positions with their support. Never split the
              difference or average competing numbers.
          3. Attach a confidence level (high, medium, low) to each major
            conclusion, with one line explaining why.
          4. Carry forward every unresolved gap. Do not let gaps disappear.

          Preserve the source URLs on every claim and conclusion.
          Work only from the analyses you are given.""",
    tools=[],
    maxTurns=5,
)

REPORT_AGENT = AgentDefinition(
    description=(
        "Turns a completed synthesis into a structured, cited research "
        "report. Use exactly once, as the final step. Cannot search."
    ),
    prompt="""You are a research report agent.
              You receive a synthesis containing conclusions, confidence levels,
              conflicts, gaps, and source URLs. Produce a report with these parts:

              - title
              - executive_summary: three to five sentences, the answer up front
              - findings: a list of claims, each with the numeric ids of the
                references that support it
              - conflicts: each conflict from the synthesis, including any left
                unresolved, described with its citations
              - limitations: confidence levels and the gaps the research did
                not cover
              - references: a numbered list, each with id, title, url, and
                publication date if known

              Citation rules, non-negotiable:
              - Cite only sources present in the synthesis you received.
                Never add a source from your own knowledge.
              - Every finding carries at least one reference id.
              - Every reference id is used by at least one finding or conflict.
              - If a claim in the synthesis has no source URL, exclude it or
                describe it in limitations as unsourced.

              Do not search the web. Do not invent, infer, or complete URLs.""",
    tools=[],
    maxTurns=5,
)

COORDINATOR_PROMPT = """You are a research coordinator managing a team
of specialist agents.

When you receive a research request:
1. Break it into focused subtasks.
2. Delegate each search subtask to search-agent, one topic per delegation.
3. Delegate each result set to analysis-agent, one analysis per topic.
4. Delegate ALL completed analyses to synthesis-agent in a single
   delegation. Include every analysis in full.
5. Delegate the complete synthesis to report-agent in a single
   delegation. Include the synthesis in full, with all URLs.
6. Return report-agent's output as your final answer, exactly as
   given. Do not edit, summarize, or reformat it.

Never search, analyze, synthesize, or write the report yourself.
Your job is delegation and assembly. Delegate only to the agents named in this workflow: search-agent,
analysis-agent, synthesis-agent, report-agent. Never delegate to any other agent type, 
including general-purpose."""


def validate_report(report: dict) -> list[str]:
    """Mechanical checks no prompt can guarantee. Returns problems found."""
    problems = []
    ref_ids = {ref["id"] for ref in report.get("references", [])}
    used_ids = set()

    if not report.get("findings"):
        problems.append("Report contains no findings.")

    for finding in report.get("findings", []):
        if not finding["citations"]:
            problems.append(f"Uncited finding: {finding['claim'][:60]}...")
        for cid in finding["citations"]:
            used_ids.add(cid)
            if cid not in ref_ids:
                problems.append(f"Citation [{cid}] has no matching reference.")

    for unused in sorted(ref_ids - used_ids):
        problems.append(f"Reference [{unused}] is never cited.")

    for ref in report.get("references", []):
        if not ref["url"].startswith("http"):
            print(f"  [warning] Reference [{ref['id']}] has a malformed URL: {ref['url']}")

    return problems


def render_markdown(report: dict) -> str:
    """Turn the validated structure into the report.md deliverable."""
    lines = [f"# {report['title']}", "", "## Executive Summary", ""]
    lines.append(report["executive_summary"])
    lines += ["", "## Findings", ""]
    for finding in report["findings"]:
        cites = ", ".join(str(c) for c in finding["citations"])
        lines.append(f"- {finding['claim']} [{cites}]")
    if report.get("conflicts"):
        lines += ["", "## Conflicting Evidence", ""]
        for conflict in report["conflicts"]:
            lines.append(f"- {conflict}")
    if report.get("limitations"):
        lines += ["", "## Confidence and Limitations", "", report["limitations"]]
    lines += ["", "## References", ""]
    for ref in report["references"]:
        date = f" ({ref['date']})" if ref.get("date") else ""
        lines.append(f"{ref['id']}. {ref['title']}{date} - {ref['url']}")
    return "\n".join(lines)


async def run_research(request: str) -> dict | None:
    options = ClaudeAgentOptions(
        system_prompt=COORDINATOR_PROMPT,
        agents={
            "search-agent": SEARCH_AGENT,
            "analysis-agent": ANALYSIS_AGENT,
            "synthesis-agent": SYNTHESIS_AGENT,
            "report-agent": REPORT_AGENT,
        },
        allowed_tools=["Agent", "WebSearch"],
        setting_sources=[],
        max_turns=35,
        max_budget_usd=4.00,
        model="claude-sonnet-5",
        fallback_model="claude-haiku-4-5-20251001",
        output_format={"type": "json_schema", "schema": REPORT_SCHEMA},
    )

    report = None
    async for message in query(prompt=request, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock) and block.name in ("Agent", "Task"):
                    agent = block.input.get("subagent_type", "unknown")
                    task = block.input.get("description", "")
                    print(f"--> Delegating to {agent}: {task}")
        elif isinstance(message, ResultMessage):
            print(f"\nRun ended: subtype={message.subtype}, "
                  f"is_error={message.is_error}, turns={message.num_turns}")
            print(f"Estimated cost: ${message.total_cost_usd:.4f}")
            if message.subtype == "success" and not message.is_error:
                report = message.structured_output
    return report

def prune_unused_references(report: dict) -> dict:
    used = {c for f in report.get("findings", []) for c in f["citations"]}
    report["references"] = [
        ref for ref in report.get("references", []) if ref["id"] in used
    ]
    return report

async def main():
    request = (
        "What does the evidence say about the impact of AI coding "
        "assistants on software developer productivity and code quality?"
    )
    report = await run_research(request)

    if report is None:
        print("Run failed before producing a report. Nothing saved.")
        return

    report = prune_unused_references(report)

    problems = validate_report(report)
    if problems:
        print("\nValidation failed:")
        for p in problems:
            print(f"  - {p}")
        print("Report NOT saved.")
        return

    with open("report.md", "w", encoding="utf-8") as f:
        f.write(render_markdown(report))
    print("\nValidation passed. Report saved to report.md")


if __name__ == "__main__":
    asyncio.run(main())