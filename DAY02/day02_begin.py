import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

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


async def run_search(topic: str) -> str:
    options = ClaudeAgentOptions(
        system_prompt=SEARCH_AGENT_PROMPT,
        allowed_tools=["WebSearch"],
        max_turns=10,
    )
    results = ""
    async for message in query(prompt=topic, options=options):
        if isinstance(message, ResultMessage):
            results = message.result or ""
    return results


async def run_analysis(search_results: str) -> str:
    options = ClaudeAgentOptions(
        system_prompt=ANALYSIS_AGENT_PROMPT,
        max_turns=3,
    )
    prompt = "Analyze these search results:\n" + search_results[:2000]
    findings = ""
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, ResultMessage):
            findings = message.result or ""
    return findings


async def main():
    topic = "The adoption of passkeys as a password replacement"
    results = await run_search(topic)
    findings = await run_analysis(results)
    print(findings)


if __name__ == "__main__":
    asyncio.run(main())