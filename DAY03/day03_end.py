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

# Subagents are defined as data: a description the coordinator uses
# to decide WHEN to delegate, a prompt that defines the specialist's
# behavior, and the tools it is allowed to touch.

SEARCH_AGENT = AgentDefinition(
    description=(
        "Searches the web for credible sources on one specific topic. "
        "Use whenever a task requires finding new information."
    ),
    prompt="""You are a research search agent.
              Search the web for the topic you are given.
              Find at least five distinct, credible sources.
              For each source report the title, URL, and a two-sentence summary.
              Do not analyze or draw conclusions. Just search and report.""",
    tools=["WebSearch"],
)

ANALYSIS_AGENT = AgentDefinition(
    description=(
        "Analyzes a set of sources and extracts key findings. "
        "Use after search results exist. Cannot search the web."
    ),
    prompt="""You are a research analysis agent.
        You receive sources found by a search agent.
        Extract the key findings:
        - The main claims that appear across multiple sources
        - Points where sources disagree
        - Gaps the sources do not cover
        Do not search the web. Work only from the sources you are given.""",
    tools=[],
)

COORDINATOR_PROMPT = """You are a research coordinator managing a team
of specialist agents.

When you receive a research request:
1. Break it into focused subtasks.
2. Delegate each search subtask to search-agent, one topic per delegation.
3. Delegate analysis of the collected results to analysis-agent.
4. Combine the analyses into one final answer.

Never search the web or analyze sources yourself. Your job is
delegation and assembly. Always report which agent handled each part."""


async def run_research(request: str) -> None:
    options = ClaudeAgentOptions(
        system_prompt=COORDINATOR_PROMPT,
        agents={
            "search-agent": SEARCH_AGENT,
            "analysis-agent": ANALYSIS_AGENT,
        },
        allowed_tools=["Agent","WebSearch"],
        setting_sources=[],
        max_turns=30,
    )

    async for message in query(prompt=request, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock) and block.name in ("Agent", "Task"):
                    agent = block.input.get("subagent_type", "unknown")
                    task = block.input.get("description", "")
                    print(f"--> Delegating to {agent}: {task}")
                elif isinstance(block, TextBlock):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            print(f"\nDone in {message.num_turns} turns.")
            print(f"Estimated cost: ${message.total_cost_usd:.4f}")


if __name__ == "__main__":
    asyncio.run(
        run_research(
             "Compare the three major approaches to running LLMs in production: "
             " commercial APIs, self-hosted open models, and cloud provider managed services. "
             " Cover cost, data privacy, and operational burden for each."
        )
    )