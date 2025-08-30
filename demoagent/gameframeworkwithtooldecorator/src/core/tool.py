
import inspect

from typing import get_type_hints, Dict, Any

from pydantic import BaseModel


# Global tool registry
class GlobalToolRegistry(BaseModel):
    tools: Dict[str, Any] = {}
    tools_by_tag: Dict[str, Any] = {}


global_tool_registry = GlobalToolRegistry()


def register_tool(tool_name=None, description=None, parameters_override=None,
                  terminal=False, tags=None):
    """
    A decorator to dynamically register a function in the tools
    dictionary with its parameters, schema, and docstring.

    Parameters:
        tool_name (str, optional): The name of the tool to register.
            Defaults to the function name.
        description (str, optional): Override for the tool's description.
            Defaults to the function's docstring.
        parameters_override (dict, optional): Override for the argument schema.
            Defaults to dynamically inferred schema.
        terminal (bool, optional): Whether the tool is terminal.
            Defaults to False.
        tags (List[str], optional): List of tags to associate with the tool.

    Returns:
        function: The wrapped function.
    """
    def decorator(func):
        metadata = get_tool_metadata(
            func=func,
            tool_name=tool_name,
            description=description,
            parameters_override=parameters_override,
            terminal=terminal,
            tags=tags
        )

        # Register the tool in global dictionary
        global_tool_registry.tools[metadata["tool_name"]] = {
            "description": metadata["description"],
            "parameters": metadata["parameters"],
            "function": metadata["function"],
            "terminal": metadata["terminal"],
            "tags": metadata["tags"] or []
        }

        # Register tool by tag
        for tag in metadata["tags"] or []:
            if tag not in global_tool_registry.tools_by_tag:
                global_tool_registry.tools_by_tag[tag] = []
            global_tool_registry.tools_by_tag[tag].append(metadata["tool_name"])

        print(f"Registered tool: '{metadata['tool_name']}' tags: {metadata['tags']}")
        return func

    return decorator


def get_tool_metadata(func, tool_name=None, description=None,
                      parameters_override=None, terminal=False,
                      tags=None) -> Dict[str, Any]:
    """
    Extracts metadata for a function to use in tool registration.

    Parameters:
        func (function): The function to extract metadata from.
        tool_name (str, optional): The name of the tool. Defaults to the function name.
        description (str, optional): Description of the tool.
            Defaults to the function's docstring.
        parameters_override (dict, optional): Override for the argument schema.
            Defaults to dynamically inferred schema.
        terminal (bool, optional): Whether the tool is terminal. Defaults to False.
        tags (List[str], optional): List of tags to associate with the tool.

    Returns:
        dict: A dictionary containing metadata about the tool, including description,
        args schema, and the function.
    """
    # Default tool_name to function_name if not provided
    tool_name = tool_name if tool_name is not None else func.__name__

    # Default description to function docstring if not provided
    description = (description
                   if description is not None
                   else func.__doc__ or "No description provided.")

    # Discover the functions signature and type hints if no args_override is provided
    if parameters_override is None:
        signature = inspect.signature(func)
        type_hints = get_type_hints(func)

        # Build the arguments schema dynamically
        args_schema = {
            "type": "object",
            "properties": {},
            "required": []
        }

        def get_json_type(param_type):
            if param_type == str:
                return "string"
            elif param_type == int:
                return "integer"
            elif param_type == float:
                return "number"
            elif param_type == bool:
                return "boolean"
            elif param_type == list:
                return "array"
            elif param_type == dict:
                return "object"
            else:
                return "string"

        for param_name, param in signature.parameters.items():
            if param_name in ["action_context", "action_agent"]:
                pass  # Skip these params

            # Add param details
            # Default to string if not annotated
            param_type = type_hints.get(param_name, str)
            # Convert Python types to JSON schema types
            param_schema = {"type": get_json_type(param_type)}

            args_schema["properties"][param_name] = param_schema

            # Add to required if not defaulted
            if param.default == inspect.Parameter.empty:
                args_schema["required"].append(param_name)
    else:
        args_schema = parameters_override

    # Return metadata as a dict
    return {
        "tool_name": tool_name,
        "description": description,
        "parameters": args_schema,
        "function": func,
        "terminal": terminal,
        "tags": tags or []
    }
