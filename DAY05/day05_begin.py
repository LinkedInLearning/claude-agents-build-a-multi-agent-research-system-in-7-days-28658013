import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AgentDefinition,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ResultMessage,
)

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
        Do not analyze or draw conclusions. Just search and report.""",
    tools=["WebSearch"],
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
        Never mention a claim without its source URLs. A claim that loses
        its URL here can never be cited downstream.
        Do not resolve disagreements. Do not search the web.""",
    tools=[],
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

        Preserve the source URLs on every claim and conclusion. A
        conclusion without its supporting URLs is unusable downstream.
        Work only from the analyses you are given.""",
    tools=[],
)

REPORT_AGENT = AgentDefinition(
    description=(
        "Turns a completed synthesis into a polished, cited research "
        "report in Markdown. Use exactly once, as the final step. "
        "Cannot search the web."
    ),
    prompt="""You are a research report agent.
        You receive a synthesis containing conclusions, confidence levels,
        conflicts, gaps, and source URLs. Write a research report in
        Markdown with this structure:

        # [Title]
        ## Executive Summary
        Three to five sentences. The answer, up front.
        ## Findings
        The conclusions, organized by theme. Every factual claim ends
        with a numbered citation like [1] or [2, 3].
        ## Conflicting Evidence
        Conflicts from the synthesis, including any left unresolved,
        with citations for each position.
        ## Confidence and Limitations
        The confidence level of each major conclusion and the gaps the
        research did not cover.
        ## References
        A numbered list. Each entry: title, URL, publication date if known.

        Citation rules, non-negotiable:
        - Cite only sources present in the synthesis you received.
          Never add a source from your own knowledge.
        - Every claim in Findings carries at least one citation number.
        - Every reference number is used at least once in the body.
        - If a claim in the synthesis has no source URL, exclude the
          claim or list it explicitly under Limitations as unsourced.

        Do not search the web. Do not invent, infer, or complete URLs.""",
    tools=[],
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
6. Output the report exactly as report-agent returned it. Do not
   edit, summarize, or reformat it.

Never search, analyze, synthesize, or write the report yourself.
Your job is delegation and assembly."""


async def run_research(request: str) -> str:
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
        max_turns=50,
    )

    report = ""
    async for message in query(prompt=request, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock) and block.name in ("Agent", "Task"):
                    agent = block.input.get("subagent_type", "unknown")
                    task = block.input.get("description", "")
                    print(f"--> Delegating to {agent}: {task}")
        elif isinstance(message, ResultMessage):
            report = message.result or ""
            print(f"\nDone in {message.num_turns} turns.")
            print(f"Estimated cost: ${message.total_cost_usd:.4f}")
    return report


async def main():
    request = (
          #TODO: Add a question of your choosing.

    )
    report = await run_research(request)

    with open("report.md", "w", encoding="utf-8") as f:
        f.write(report)
    print("\nReport saved to report.md")


if __name__ == "__main__":
    asyncio.run(main())