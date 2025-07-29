import asyncio
from agents import Agent, InputGuardrail, Runner, function_tool
from agents.exceptions import InputGuardrailTripwireTriggered
from dotenv import load_dotenv

from guardrail_agent import (
    is_valid_addition_or_subtraction_or_multiplication_operation_guardrail,
)

load_dotenv()

openai_model_gpt41 = "gpt-4.1"


@function_tool
def multiply_two_numbers(num1: int, num2: int) -> int:
    """
    Given two numbers, returns multiplication result
    Args:
        num1: number one
        num2: number two
    Output: The multiplication result
    """
    print(f"Multiplcation via tool calling: {num1} * {num2}")
    return num1 * num2


addition_agent = Agent(
    name="AdditionCalculatorAgent",
    instructions="You are a calculator who can only do addition of two numbers.",
    model=openai_model_gpt41,
)

subtraction_agent = Agent(
    name="SubtractionCalculatorAgent",
    instructions="You are a calculator who can only do subtraction of two numbers.",
    model=openai_model_gpt41,
)

multiplication_agent = Agent(
    name="MultiplicationCalculatorAgent",
    instructions="You are a calculator who can only use the tools provided to perform operations \
        and returns the result which you got from tool calling without modification",
    model=openai_model_gpt41,
    tools=[multiply_two_numbers],
)

orchestrator_handsoff_agent = Agent(
    name="AgentOrchestrator",
    instructions=(
        "You determine which agent to call based on addition or subtraction user wants to perform"
        "If user want to perform addition, handoff to addition_agent"
        "If user want to perform subtraction, handoff to subtraction_agent"
        "If user want to perform multiplication, handoff to multiplication_agent"
    ),
    handoffs=[addition_agent, subtraction_agent, multiplication_agent],
    input_guardrails=[
        InputGuardrail(
            guardrail_function=is_valid_addition_or_subtraction_or_multiplication_operation_guardrail
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
    # await simple_handsoff_agent("2 - 3")
    # await simple_handsoff_agent("2 + 3")
    await simple_handsoff_agent("2 * 5")


if __name__ == "__main__":
    asyncio.run(main())
