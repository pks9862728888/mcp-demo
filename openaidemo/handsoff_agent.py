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


def simple_handsoff_agent():
    result = Runner.run_sync(orchestrator_handsoff_agent, input="2 - 3")
    print(result)
    print(result.final_output)


def main():
    simple_handsoff_agent()


if __name__ == "__main__":
    main()
