from langchain_core.output_parsers import PydanticToolsParser

import json
from openai import BaseModel
from pydantic import Field
from app.model import model


class add(BaseModel):
    """Add two integers."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


class multiply(BaseModel):
    """Multiply two integers."""
    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


def tool_execution_demo(prompt):
    """
    If you pipe tool calling with parser it will auto parse
    """
    model_with_tools = model.bind_tools([multiply, add])
    # only first tool will be used
    chain = model_with_tools | PydanticToolsParser(tools = [multiply, add]) 
    response = chain.invoke(prompt)
    print(response[0])
    print(response[0].a)
    print(response[0].b)
