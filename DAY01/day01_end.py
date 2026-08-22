import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ResultMessage,
)

SEARCH_AGENT_PROMPT = """You are a research search agent.
                      Your job: search the web for the topic you are given.
                      Return your findings as a list. For each finding include:
                        - The source title and URL
                        - A two-sentence summary of what the source says
                      Find at least five distinct, credible sources.
                      Do not analyze or draw conclusions. Just search and report."""


async def run_search_agent(topic: str) -> None:
    options = ClaudeAgentOptions(
        system_prompt=SEARCH_AGENT_PROMPT,
        allowed_tools=["WebSearch"],
        max_turns=10,
    )

    # Agentic loop: streams messages as Claude works
    async for message in query(prompt=topic, options=options):
        # Print human-readable output
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            print(f"\nDone in {message.num_turns} turns.")
            print(f"Estimated cost: ${message.total_cost_usd:.4f}")

if __name__ == "__main__":
    asyncio.run(run_search_agent("The current state of quantum computing"))