import json
from dotenv import load_dotenv
from litellm import completion
from pydantic import BaseModel, Field
from typing import Dict, List


load_dotenv()


class Prompt(BaseModel):
    messages: List[Dict] = Field(default_factory=list)
    tools: List[Dict] = Field(default_factory=list)
    metadata: Dict = Field(default_factory=dict)


def generate_response(prompt: Prompt) -> str | Dict:
    """Calls llm to generate response"""
    messages = prompt.messages
    tools = prompt.tools

    # Call the llm
    if not tools:
        response = completion(
            model="openai/gpt-4o",
            messages=messages,
            max_tokens=1024
        )
    else:
        response = completion(
            model="openai/gpt-4o",
            messages=messages,
            tools=tools,
            max_tokens=1024
        )

    result = {}
    if response.choices[0].message.tool_calls:  # type: ignore
        tool = response.choices[0].message.tool_calls[0]  # type: ignore
        try:
            result = {
                "tool": tool.function.name,
                "args": json.loads(tool.function.arguments)
            }
        except json.JSONDecodeError as e:
            result = {
                "tool": tool.function.name,
                "error": f"Error decoding JSON args: {tool.function.arguments}, ex: {e}"
            }
    else:
        result = response.choices[0].message.content  # type: ignore
        result = result if result is not None else ""

    return result
