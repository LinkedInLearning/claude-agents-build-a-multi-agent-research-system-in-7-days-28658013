import asyncio
import json
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

SEARCH_AGENT_PROMPT = """You are a research search agent.
                      Your job: search the web for the topic you are given.
                      Return your findings as a list. For each finding include:
                      - The source title and URL
                      - A two-sentence summary of what the source says
                      Find at least five distinct, credible sources.
                      Do not analyze or draw conclusions. Just search and report."""

async def run_search(topic: str) -> str:
    """Run the search agent. Returns validated, structured results."""
    options = ClaudeAgentOptions(
        system_prompt=SEARCH_AGENT_PROMPT,
        allowed_tools=["WebSearch"],
        max_budget_usd=4.00,
        model="claude-sonnet-5",
        fallback_model="claude-haiku-4-5-20251001",
        max_turns=10
    )
    output = None
    
    async for message in query(prompt=topic, options=options):
        if isinstance(message, ResultMessage):
            output = message.result

    if output is None:
        raise RuntimeError("Search agent returned no output")
    return output

async def main():
    topic = "The current state of small modular nuclear reactors"
    print("Search agent working...\n")
    results = await run_search(topic)
    print(results)

if __name__ == "__main__":
    asyncio.run(main())