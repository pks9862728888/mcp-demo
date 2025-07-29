import asyncio
from typing import final
from agents import (
    Agent,
    AgentOutputSchema,
    GuardrailFunctionOutput,
    InputGuardrail,
    Runner,
    guardrail,
)
from agents.exceptions import InputGuardrailTripwireTriggered
from dotenv import load_dotenv
from openai import BaseModel
from datetime import date

from pydantic import ConfigDict

from guardrail_agent import ValidOperationOutput

load_dotenv()

openai_model_gpt41 = "gpt-4.1"


class CalendarEvent(BaseModel):
    organizer: str
    date: date
    occassion: str
    attendees: list[str]

    model_config = ConfigDict(extra="forbid")


guardrail_calendar_event = Agent(
    name="GuardrailCalendarEvent",
    instructions="Check if prompt is of type calendar event containing organizer, date, occassion and attendees",
    output_type=AgentOutputSchema(ValidOperationOutput, strict_json_schema=True),
)


async def is_valid_calendar_event(ctx, agent, input_data):
    result = await Runner.run(guardrail_calendar_event, input_data, context=ctx.context)
    final_output: ValidOperationOutput = result.final_output_as(ValidOperationOutput)
    return GuardrailFunctionOutput(
        output_info=final_output, tripwire_triggered=not final_output.is_valid_operation
    )


calendar_event_extractor_agent = Agent(
    name="CalendarEventExtractorAgent",
    instructions="Extract calendar event from text",
    model=openai_model_gpt41,
    output_type=CalendarEvent,
)

calendar_event_extractor_handsoff_agent = Agent(
    name="CalendarEventOrchastrator",
    instructions="You determine which agent to call based on user prompt, validate input using guardrail before calling",
    handoffs=[calendar_event_extractor_agent],
    input_guardrails=[InputGuardrail(guardrail_function=is_valid_calendar_event)],
)


async def get_calendar_event_from_text(prompt: str):
    """
    Extracts calendar event from text
    """
    print(prompt)
    try:
        result = await Runner.run(calendar_event_extractor_handsoff_agent, input=prompt)
        print(result)
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print(f"Guardrail triggered for input: {prompt}, {e.guardrail_result}")
    print()


async def main():
    await get_calendar_event_from_text(
        "Birthday Event is organized by Penny on March 12, 2025, and Ami and Sheldon are invited"
    )
    await get_calendar_event_from_text("How far is Hyderabad from Bangalore?")


if __name__ == "__main__":
    asyncio.run(main())
