from typing import Any, Dict, List
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

def generate_response(messages: List[Dict]) -> str:
    response = completion(
        model="openai/gpt-4o",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content # type: ignore


def extract_markdown_block(response: str, block_type: str = "json") -> str:
    """Extract code block from response"""

    if not '```' in response:
        return response

    code_block = response.split('```')[1].strip()

    if code_block.startswith(block_type):
        code_block = code_block[len(block_type):].strip()

    return code_block


def parse_action(llm_response: str) -> Dict[str, Any]:
    """Parse the LLM response into a structured action dictionary."""
    try:
        response = extract_markdown_block(llm_response, "action")
        response_json = json.loads(response)
        if "tool_name" in response_json and "args" in response_json:
            return response_json
        else:
            return {"tool_name": "error", "args": {"message": "You must respond with a JSON tool invocation."}}
    except json.JSONDecodeError:
        return {"tool_name": "error", "args": {"message": "Invalid JSON response. You must respond with a JSON tool invocation."}}


def read_file(file_name: str | None) -> Dict[str, str]:
    if not file_name:
        return {"error": "No file name provided"}
    file_path = os.path.join("files", file_name)
    try:
        print(f"Reading file content: {file_path}")
        with open(file_path, "r") as f:
            return {"file_content": f.read(), "file_name": file_name}
    except FileNotFoundError:
        return {"error": f"File not found: {file_path}"}


def rag_agent_in_loop_demo():
    messages = [{
    "role": "system",
    "content": """
    You are an AI agent that can perform tasks by using available tools.

    Available tools:

    ```json
    {
        "list_files": {
            "description": "Lists all files in the current directory.",
            "parameters": {}
        },
        "read_file": {
            "description": "Reads the content of a file.",
            "parameters": {
                "file_name": {
                    "type": "string",
                    "description": "The name of the file to read."
                }
            }
        },
        "terminate": {
            "description": "Ends the agent loop and provides a summary of the task.",
            "parameters": {
                "message": {
                    "type": "string",
                    "description": "Summary message to return to the user."
                }
            }
        }
    }
    ```

    If a user asks about files, documents, or content, first list the files before reading them.

    When you are done, terminate the conversation by using the "terminate" tool and I will provide the results to the user.

    Important!!! Every response MUST have an action.
    You must ALWAYS respond in this format:

    <Stop and think step by step. Parameters map to args. Insert a rich description of your step by step thoughts here.>

    ```action
    {
        "tool_name": "insert tool_name",
        "args": {...fill in any required arguments here...}
        "reasoning": "Explain why this action is being taken."
        "confidence": "0-1"
    }
    ```"""
    }]

    max_iterations: int = 5
    iterations: int = 0
    user_input = input("What do you want to know? ")
    messages.append({"role": "user", "content": user_input})

    while iterations < max_iterations:
        # Send prompt to LLM to determine an action
        print("Agent thinking...")
        response = generate_response(messages)
        action_response = parse_action(response)
        print("Agent action response:", action_response)
        messages.append({"role": "assistant", "content": json.dumps(action_response)})

        # Parse the action to be taken and take action, report action outcome to agent
        action_name = action_response.get("tool_name", None)
        if action_name == "terminate":
            print(f"{action_response.get('result', '')}")
            print("Terminating...")
            break
        elif action_name == "list_files":
            print("Listing files...")
            files = os.listdir("files")
            messages.append({"role": "user", "content": json.dumps({"files": files})})
            print(f"files: {files}")
        elif action_name == "read_file":
            file_name = action_response.get("args", {}).get("file_name", None)
            file_content_response = read_file(file_name)
            messages.append({"role": "user", "content": json.dumps(file_content_response)})
            print(f"file_content: {file_content_response}")
        elif action_name == "display_error":
            error_message = action_response.get("args", {}).get("error", "Unknown error")
            print(error_message)
            messages.append({"role": "user", "content": f"Error communicated to user: {json.dumps({'error': error_message})}"})
        else:
            print(f"Invalid action_type: {action_name}")
            break

        iterations += 1


if __name__ == "__main__":
    rag_agent_in_loop_demo()
