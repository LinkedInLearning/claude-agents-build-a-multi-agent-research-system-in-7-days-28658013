import asyncio
import json
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

# The contract: this schema defines exactly what the search agent
# must return and what the analysis agent can rely on receiving.
SEARCH_SCHEMA = {
    "type": "object",
    "properties": {
        "sources": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "url": {"type": "string"},
                    "summary": {"type": "string"},
                },
                "required": ["title", "url", "summary"],
            },
        }
    },
    "required": ["sources"],
}

SEARCH_AGENT_PROMPT = """You are a research search agent.
Search the web for the topic you are given.
Find at least five distinct, credible sources.
Write up your findings in a readable report for your teammate."""

ANALYSIS_AGENT_PROMPT = """You are a research analysis agent.
                        You receive a JSON object containing sources found by a search agent.
                        Extract the key findings:
                            - The main claims that appear across multiple sources
                            - Points where sources disagree
                            - Gaps the sources do not cover
                        Do not search the web. Work only from the sources you are given."""

async def run_search(topic: str) -> dict:
    """Run the search agent. Returns validated, structured results."""
    options = ClaudeAgentOptions(
        system_prompt=SEARCH_AGENT_PROMPT,
        allowed_tools=["WebSearch"],
        max_turns=10,
        output_format={"type": "json_schema", "schema": SEARCH_SCHEMA},
    )
    output = None
    async for message in query(prompt=topic, options=options):
        if isinstance(message, ResultMessage):
            output = message.structured_output
    if output is None:
        raise RuntimeError("Search agent returned no structured output")
    return output


async def run_analysis(search_results: dict) -> str:
    """Run the analysis agent on the search agent's output."""
    options = ClaudeAgentOptions(
        system_prompt=ANALYSIS_AGENT_PROMPT,
        max_turns=3,
    )
    prompt = "Analyze these search results:\n" + json.dumps(search_results, indent=2)
    findings = None
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, ResultMessage):
            findings = message.result
    if findings is None:
        raise RuntimeError("Analysis agent did not complete")
    return findings

async def main():
    topic = "The current state of small modular nuclear reactors"

    print("Search agent working...")
    results = await run_search(topic)
    print(f"Search agent returned {len(results['sources'])} sources.\n")

    print("Analysis agent working...\n")
    findings = await run_analysis(results)
    print(findings)


if __name__ == "__main__":
    asyncio.run(main())