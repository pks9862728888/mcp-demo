from pydantic import BaseModel, Field
from app.model import model


class ResponseFormatter(BaseModel):
    answer: str = Field(description="The answer to the user's question")
    followup_question: str = Field(description="A followup question the user could ask")


def structured_output_tool_calls(user_input):
    """
    simply bind our schema to a model as a tool,
    response will be tool call output, but manually output needs to be parsed to schema
    """
    model_with_structure = model.bind_tools([ResponseFormatter])
    response = model_with_structure.invoke(user_input)
    tool_calls = getattr(response, 'tool_calls', None)
    if tool_calls:
        # print(tool_calls[0]["args"])
        # Manually parse the output to the schema
        parsed_output = ResponseFormatter(**tool_calls[0]["args"])
        print(parsed_output)


def structured_output_json_mode(user_input):
    """
    Model will respond to our question with the schema which we specified
    """
    model_with_structured_output = model.with_structured_output(schema=ResponseFormatter)
    response = model_with_structured_output.invoke(user_input)
    print(response)
