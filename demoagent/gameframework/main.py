from src.core.prompt import generate_response
from src.core.goal import Goal
from src.core.agent_language import AgentFunctionCallingAgentLanguage
from src.core.action import Action, ActionRegistry
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
             description="Call the terminate call when you have read all the files "
             "and provide the content of the README in the terminate message")
    ]

    # Define agents language
    agent_language = AgentFunctionCallingAgentLanguage()

    # Define agent tools
    def read_project_file(name: str) -> Dict[str, str]:
        """Read the content of a file in the project"""
        try:
            with open(name, 'r') as file:
                return {"content": file.read()}
        except FileNotFoundError:
            return {"error": f"File {name} not found."}

    def list_project_files() -> List[str]:
        """Lists project python files"""
        return sorted([file for file in os.listdir(".") if file.endswith(".py")])

    # Define action registry
    action_registry = ActionRegistry()
    action_registry.register(
        Action(name="list_project_files",
               function=list_project_files,
               description="List all python files in the project",
               parameters={},
               terminal=False))
    action_registry.register(
        Action(name="read_project_file",
               function=read_project_file,
               description="Read a specific file from project",
               parameters={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the file to read"
                        }
                    },
                    "required": ["name"]
                }, terminal=False))
    action_registry.register(
        Action(name="terminate",
               function=lambda message: {"message": message},
               description="Terminate the agent's execution with a final message",
               parameters={
                   "type": "object",
                   "properties": {
                       "message": {
                           "type": "string",
                           "description": "The termination message for the user"
                        }
                    }, "required": ["message"]
                }, terminal=True))

    # Define an environment
    environment = Environment()

    # Create an agent
    agent = Agent(goals=goals,
                  agent_language=agent_language,
                  action_registry=action_registry,
                  generate_response=generate_response,
                  environment=environment)

    # Run the agent with user input
    user_input = "Write a README for this project"
    final_memory = agent.run(user_input=user_input)

    # Print final memory
    print(final_memory.get())


if __name__ == "__main__":
    main()
