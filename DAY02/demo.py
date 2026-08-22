import asyncio
import json
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

# The contract: this schema defines exactly what the search agent
# must return and what the analysis agent can rely on receiving.
#TODO: SCHEMA HERE
SEARCH_SCHEMA = { 
}

SEARCH_AGENT_PROMPT = """You are a research search agent.
Search the web for the topic you are given.
Find at least five distinct, credible sources.
Write up your findings in a readable report for your teammate."""

#TODO: PROMPT HERE
ANALYSIS_AGENT_PROMPT = """  TODO: PROMPT HERE """

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

#TODO: run_analysis(search_results: dict) -> str: HERE

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