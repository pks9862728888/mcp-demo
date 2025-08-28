from typing import List, Callable, Dict, Tuple
from src.core.goal import Goal
from src.core.action import Action, ActionRegistry, ActionResult
from src.core.agent_language import AgentLanguage
from src.core.prompt import Prompt
from src.core.environment import Environment
from src.core.memory import Memory

import json


class Agent:
    def __init__(self,
                 goals: List[Goal],
                 agent_language: AgentLanguage,
                 action_registry: ActionRegistry,
                 generate_response: Callable[[Prompt], str | dict],
                 environment: Environment):
        """Initialize an agent with core GAME components"""
        self.goals = goals
        self.agent_language = agent_language
        self.action_registry = action_registry
        self.generate_response = generate_response
        self.environment = environment

    def construct_prompt(self, memory: Memory) -> Prompt:
        """Build prompt with memory context"""
        return self.agent_language.construct_prompt(
            self.action_registry.list_actions(),
            self.goals,
            memory)

    def get_action(self, response: str | Dict | None) -> Tuple[Action | None, Dict]:
        """Return the action"""
        if response is None:
            return None, {}
        invocation = self.agent_language.parse_response(response)
        action = self.action_registry.get(invocation["tool"])
        return action, invocation

    def should_terminate(self, response: str | Dict | None) -> bool:
        """Check if the agent should terminate"""
        action, _ = self.get_action(response)
        return action.terminal if action else False

    def set_current_task(self, memory: Memory, task: str):
        """Set the current task in memory"""
        memory.append({"type": "user", "content": task})

    def update_memory(self, memory: Memory, response: str | Dict, result: ActionResult):
        """Update memory with response and result"""
        formatted_response = json.dumps(response) \
            if isinstance(response, dict) else response
        memory.append({"type": "assistant", "content": formatted_response})
        memory.append({"type": "environment",
                       "content": json.dumps(result.model_dump_json())})

    def prompt_llm_for_action(self, prompt: Prompt) -> str | Dict:
        return self.generate_response(prompt)

    def run(self,
            user_input: str,
            memory: Memory = Memory(),
            max_iterations: int = 50) -> Memory:
        """Execute the GAME loop for this agent till max iteration limit"""
        self.set_current_task(memory, user_input)
        for _ in range(max_iterations):
            # Construct prompt
            prompt: Prompt = self.construct_prompt(memory)

            # Generate a response from agent
            print("\nAgent thinking...")
            response: str | Dict = self.prompt_llm_for_action(prompt)
            print(f"Agent decision: {response}")

            # Determine action to execute
            action, invocation = self.get_action(response)

            # Execute the action in environment
            if action:
                result: ActionResult = self.environment.execute_action(
                    action, invocation["args"])
            else:
                result: ActionResult = ActionResult(
                    error="Action could not be determined from response")
            print(f"Agent result: {result}")

            # Update agents memory with the information of what happened
            self.update_memory(memory, response, result)

            # Terminate if agent has decided to terminate
            if self.should_terminate(response):
                print("Agent has decided to terminate.")
                break

        return memory
