from typing import final
from agents import Agent, GuardrailFunctionOutput, Runner
from agents.agent_output import AgentOutputSchema
from dotenv import load_dotenv
from openai import BaseModel
from pydantic import ConfigDict

load_dotenv()


class ValidOperationOutput(BaseModel):
    is_valid_operation: bool
    reasoning: str

    model_config = ConfigDict(extra="forbid", strict=True)


guardrail_agent = Agent(
    name="OperatorGuardrailAgent",
    instructions="Check if user is trying to do addition or subtraction",
    output_type=AgentOutputSchema(ValidOperationOutput, strict_json_schema=True),
)


async def is_valid_addition_or_subtraction_operation_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output: ValidOperationOutput = result.final_output_as(ValidOperationOutput)
    # print(final_output)
    return GuardrailFunctionOutput(
        output_info=final_output, tripwire_triggered=not final_output.is_valid_operation
    )
