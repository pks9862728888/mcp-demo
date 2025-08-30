from src.core.tool import register_tool
from src.core.prompt import generate_response
from src.core.goal import Goal
from src.core.agent_language import AgentFunctionCallingAgentLanguage
from src.core.action import PythonActionRegistry
from src.core.environment import Environment
from src.core.agent import Agent

import os
from typing import Dict, List


def main():
    # Define agents goal
    goals = [
        Goal(priority=1,
             name="Gather Information",
             description="Read each file in the project"),
        Goal(priority=1,
             name="Terminate",
             description="Call terminate when done and "
             "provide a complete README for the project in the message parameter")
    ]

    # Define agents language
    agent_language = AgentFunctionCallingAgentLanguage()

    # Define agent tools
    @register_tool(tags=["file_operations", "read"])
    def read_project_file(name: str) -> Dict[str, str]:
        """Reads and returns the content of a specified project file.

        Opens the file in read mode and returns its entire contents as a string.
        Raises FileNotFoundError if the file doesn't exist.

        Args:
            name: The name of the file to read

        Returns:
            The contents of the file as a string
        """
        try:
            with open(name, 'r') as file:
                return {"content": file.read()}
        except FileNotFoundError:
            return {"error": f"File {name} not found."}

    @register_tool(tags=["file_operations", "list"])
    def list_project_files() -> List[str]:
        """Lists all Python files in the current project directory.

        Scans the current directory and returns a sorted list of all files
        that end with '.py'.

        Returns:
            A sorted list of Python filenames
        """
        return sorted([file for file in os.listdir(".") if file.endswith(".py")])

    @register_tool(tags=["system"], terminal=True)
    def terminate(message: str) -> str:
        """Terminates the agent's execution with a final message.

        Args:
            message: The final message to return before terminating

        Returns:
            The message with a termination note appended
        """
        return f"{message}\nTerminating..."

    # Define an environment
    environment = Environment()

    # Create an agent
    agent = Agent(agent_name="ProjectFileAgent",
                  goals=goals,
                  agent_language=agent_language,
                  action_registry=PythonActionRegistry(
                      tags=["file_operations", "system"]),
                  generate_response=generate_response,
                  environment=environment)

    # Run the agent with user input
    user_input = "Write a README for this project"
    final_memory = agent.run(user_input=user_input)

    # Print final memory
    print(final_memory.get())


if __name__ == "__main__":
    main()
