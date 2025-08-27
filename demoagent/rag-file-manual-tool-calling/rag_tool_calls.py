from typing import Dict, List, Union
from dotenv import load_dotenv
import os
import json

from litellm import completion

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")
else:
    print("OPENAI_API_KEY is set")


def list_files() -> List[str]:
    """List files in the files directory."""
    return os.listdir("files")


def read_file(file_name: str | None) -> Dict[str, str]:
    """Read a file's contents."""
    if not file_name:
        return {"error": "No file name provided"}
    file_path = os.path.join("files", file_name)
    try:
        print(f"Reading file content: {file_path}")
        with open(file_path, "r") as f:
            return {"file_content": f.read(), "file_name": file_name}
    except FileNotFoundError:
        return {"error": f"File not found: {file_path}"}


def terminate(result: str) -> str:
    """Return the final result to terminate the process."""
    return result


def rag_agent_in_loop_demo():
    tool_functions = {
        "list_files": list_files,
        "read_file": read_file,
        "terminate": terminate
    }
    tools = [
        {
            "type": "function",
            "function": {
                "name": "list_files",
                "description": "Lists all files in the directory",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read the content of specified file in the directory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "description": "The name of the file to read."
                        },
                    },
                    "required": ["file_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "terminate",
                "description": "Terminates the conversation. \
                    No further actions or interactions are possible after this. \
                        Prints the provided message for the user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "result": {
                            "type": "string",
                            "description": "The final message to communicate to user"
                        },
                    },
                    "required": ["result"]
                }
            }
        }
    ]
    messages = [{
    "role": "system",
    "content": """
    You are an AI agent that can perform tasks by using available tools.

    For responding to users query, first list the files before reading them. Only list_files once in the beginning.
    
    When you are done, terminate the conversation by using the "terminate" tool and I will provide the results to the user.
    """}]

    max_iterations: int = 5
    iterations: int = 0
    user_input = input("What do you want to know? ")
    messages.append({"role": "user", "content": user_input})

    while iterations < max_iterations:
        # Send prompt to LLM to determine an action
        iterations += 1
        print("\nAgent thinking...")
        response = completion(
            model="openai/gpt-4o",
            messages=messages,
            tools=tools,
            max_tokens=1024
        )
        if (response.choices[0].message.tool_calls): # type: ignore
            tool = response.choices[0].message.tool_calls[0] # type: ignore
            tool_name = tool.function.name
            try:
                tool_args = json.loads(tool.function.arguments)
            except json.JSONDecodeError as e:
                tool_args = {}
                messages.append({"role": "assistant", "content": f"Error decoding JSON tool_args for {tool_name}: {e}"})
                continue
            print(f"Agent selected tool: {tool_name} with args: {tool_args}")

            action = {
                "tool_name": tool_name,
                "args": tool_args
            }

            # Call function
            if tool_name == "terminate":
                print("Final result:", tool_args["result"])
                break
            elif tool_name in tool_functions:
                try:
                    result = tool_functions[tool_name](**tool_args)
                    print(f"Agent tool: {tool_name} calling response: {result}")
                except Exception as e:
                    result = {"error": f"Error executing {tool_name}, error_message: {str(e)}"}
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
            messages.append({"role": "assistant", "content": json.dumps(action)})
            messages.append({"role": "user", "content": json.dumps(result)})
        else:
            result = response.choices[0].message.content # type: ignore
            print("Agent response:", result)
            break


if __name__ == "__main__":
    rag_agent_in_loop_demo()
