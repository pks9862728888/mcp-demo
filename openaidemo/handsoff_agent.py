import asyncio
from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

addition_agent = Agent(
    name="AdditionCalculatorAgent",
    instructions="You are a calculator who can only do addition of two numbers.",
    model="gpt-4.1",
)

subtraction_agent = Agent(
    name="SubtractionCalculatorAgent",
    instructions="You are a calculator who can only do subtraction of two numbers.",
    model="gpt-4.1",
)

orchestrator_handsoff_agent = Agent(
    name="AgentOrchestrator",
    instructions="You determine which agent to call based on addition or subtraction user wants to perform",
    handoffs=[addition_agent, subtraction_agent],
    handoff_description=[
        "Useful when addition of two numbers is intended",
        "Useful when subtraction of two numbers is requried",
    ],
)


async def simple_handsoff_agent(prompt: str):
    print(prompt)
    result = await Runner.run(orchestrator_handsoff_agent, input=prompt)
    print(result)
    print(result.final_output)
    print()


async def main():
    await simple_handsoff_agent("2 - 3")
    await simple_handsoff_agent("2 + 3")
    await simple_handsoff_agent("2 plus 5")


if __name__ == "__main__":
    asyncio.run(main())
