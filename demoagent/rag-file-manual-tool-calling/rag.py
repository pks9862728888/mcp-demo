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


def parse_action(llm_response: str) -> Dict[str, Any]:
    try:
        response = json.loads(llm_response)
    except json.JSONDecodeError:
        response = {"error": "Invalid JSON format"}
    return response


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
    messages = [
        {"role": "system", 
         "content": """
         You are a helpful assistant. 

         Based on user's input you can take one of the following actions:
         1. list_files
         2. read_file
         3. display_error
         4. terminate

         The action which you choose from above should be output in JSON format: 
         {"action_name": "action_name_from_above_list", "action_param": "action_param", "result": "final result to dislay to user if action_type is terminate", "reasoning": "reasoning why you have chosen that action", "error": "error_message", "confidence": "0-1"}
         For each response only output in above json format only, do not include any additional text.

         If you haven't listed files initially, then always first list_files to know what are the available files. 
         Once you have got the files, based on file_name decide which files are relevant.
         Once you have decided the relevant files, you can use read_file to read content of file.
         Once you have read conent of file, you can use the context from files to answer user queries.

         If no relevant files are found, or if content of file is not sufficient to answer user's query
         then clearly communicate this to the user and terminate the action loop.
         """}
    ]

    max_iterations: int = 5
    iterations: int = 0
    user_input = input("What do you want to know?")
    messages.append({"role": "user", "content": user_input})

    while iterations < max_iterations:
        # Send prompt to LLM to determine an action
        print("Agent thinking...")
        response = generate_response(messages)
        action_response = parse_action(response)
        print("Agent action response:", action_response)
        messages.append({"role": "assistant", "content": json.dumps(action_response)})

        # Parse the action to be taken and take action, report action outcome to agent
        action_name = action_response.get("action_name", None)
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
            file_name = action_response.get("action_param", None)
            file_content_response = read_file(file_name)
            messages.append({"role": "user", "content": json.dumps(file_content_response)})
            print(f"file_content: {file_content_response}")
        elif action_name == "display_error":
            error_message = action_response.get("error", action_response.get("error", "Unknown error"))
            print(error_message)
            messages.append({"role": "user", "content": f"Error communicated to user: {json.dumps({'error': error_message})}"})
        else:
            print(f"Invalid action_type: {action_name}")
            break

        iterations += 1


if __name__ == "__main__":
    rag_agent_in_loop_demo()
