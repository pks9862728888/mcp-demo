import asyncio
from agents import Agent, InputGuardrail, Runner
from agents.exceptions import InputGuardrailTripwireTriggered
from dotenv import load_dotenv

from guardrail_agent import is_valid_addition_or_subtraction_operation_guardrail

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
    # handoff_description=[
    #     "Useful when addition of two numbers is intended",
    #     "Useful when subtraction of two numbers is requried",
    # ],
    input_guardrails=[
        InputGuardrail(
            guardrail_function=is_valid_addition_or_subtraction_operation_guardrail
        )
    ],
)


async def simple_handsoff_agent(prompt: str):
    """
    Handsoff agent can delegate task to multiple agents based on decision made by orchestrator
    """
    print(prompt)
    try:
        result = await Runner.run(orchestrator_handsoff_agent, input=prompt)
        print(result)
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print(f"Guardrail blocked input: {prompt}", e.guardrail_result)
    print()


async def main():
    await simple_handsoff_agent("2 - 3")
    await simple_handsoff_agent("2 / 3")
    await simple_handsoff_agent("2 + 3")
    await simple_handsoff_agent("2 plus 5")


if __name__ == "__main__":
    asyncio.run(main())
