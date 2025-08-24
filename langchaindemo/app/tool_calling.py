from app.model import model
from langchain_core.tools import tool
from langchain_core.output_parsers import PydanticToolsParser
import json

@tool
def multiply(a: int, b: int) -> str:
    """
    Multiply two numbers,
    Args:
        a (int): The first number.
        b (int): The second number.
    """
    return f"Mul res = {a * b}"


@tool
def add(a: int, b: int) -> str:
    """
    Add two numbers,
    Args:
        a (int): The first number.
        b (int): The second number.
    """
    return f"Add res = {a + b}"


def tool_calling_force_binding(prompt):
    """
    Will force bind model to specific tool
    If prompt does not need tool calling, then also it will go for tool calling,
    tool_choice = any will choose any tool
    tool_choice = auto will automatically choose the best tool for the task, 
        it might not even use the tools
    """
    model_with_tools = model.bind_tools([add], tool_choice="add")
    response = model_with_tools.invoke(prompt)
    print(json.dumps(response.to_json(), indent=2))
    print()


def tool_calling_demo(prompt):
    """If tool calling is required, tool_calls will have everyting required to call a tool
    "tool_calls": [
      {
        "name": "add",
        "args": {
          "a": 5,
          "b": 3
        },
        "id": "call_ORobdLVdTcOt8jdOLyXnxAWu",
        "type": "tool_call"
      },
    ],
    """
    model_with_tools = model.bind_tools([multiply, add])
    response = model_with_tools.invoke(prompt)
    print(json.dumps(response.to_json(), indent=2))
    print()

