import asyncio
from typing import final

from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrail,
    ModelSettings,
    Runner,
    function_tool,
)
from agents.exceptions import InputGuardrailTripwireTriggered
from dotenv import load_dotenv

from guardrail_agent import ValidOperationOutput

load_dotenv()


@function_tool
def get_weather(city: str) -> str:
    """
    Returns current weather of city
    Args:
    city: The city for which weather is to be found
    """
    return f"The weather in city: {city} is sunny."


guardrail_agent = Agent(
    name="WeatherFetcherGuardrail",
    instructions="Check if user is trying to know wether details",
    output_type=ValidOperationOutput,
)


async def validate_input(ctx, agent, prompt):
    result = await Runner.run(guardrail_agent, prompt, context=ctx.context)
    final_output: ValidOperationOutput = result.final_output_as(ValidOperationOutput)
    return GuardrailFunctionOutput(
        output_info=final_output, tripwire_triggered=not final_output.is_valid_operation
    )


agent = Agent(
    name="WeatherFetcherAgent",
    instructions="Validate input using guardrail first and if guardrail is not triggered then retrieve weather details",
    tools=[get_weather],
    model_settings=ModelSettings(tool_choice="get_weather"),
    input_guardrails=[InputGuardrail(guardrail_function=validate_input)],
)


async def run_force_tool_use(prompt: str):
    print(prompt)
    try:
        result = await Runner.run(agent, input=prompt)
        print(result)
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print(f"Guardrail: {e.guardrail_result}")
    print()


async def main():
    await run_force_tool_use("What is weather in Paris?")
    await run_force_tool_use("What is the capital of India?")


if __name__ == "__main__":
    asyncio.run(main())
