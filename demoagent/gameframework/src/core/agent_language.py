import json
from typing import Any, List, Dict
from core.action import Action
from core.goal import Goal
from core.memory import Memory
from core.prompt import Prompt


class AgentLanguage:
    def __init__(self):
        pass

    def construct_prompt(self,
                         actions: List[Action],
                         goals: List[Goal],
                         memory: Memory) -> Prompt:
        raise NotImplementedError("construct_prompt not implemented.")

    def parse_response(self, response: str | Dict) -> Dict:
        raise NotImplementedError("parse_response not implemented.")


class AgentFunctionCallingAgentLanguage(AgentLanguage):
    def __init__(self):
        super().__init__()

    def format_goals(self, goals: List[Goal]) -> List[Dict]:
        """
        Map all goals to a single line that concatenates
        their description and combine to single system message
        """
        sep = "\n----------------------\n"
        return [{"role": "system", "content":
                 "\n\n".join(f"{goal.name}:{sep}:{goal.description}:{sep}"
                             for goal in goals)}]

    def format_memory(self, memory: Memory) -> List[Dict]:
        """
        Map all environment and assistant results to role:assistant messages
        Map all user results to role:user messages
        """
        memories = memory.get()
        mapped_memories = []
        for memory_item in memories:
            role = memory_item["type"]
            content = memory_item["content"]
            if role == "assistant" or role == "environment":
                mapped_memories.append({"role": "assistant", "content": content})
            else:
                mapped_memories.append({"role": "user", "content": content})
        return mapped_memories

    def format_actions(self, actions: List[Action]) -> List[Dict]:
        """Generate response from language model"""
        tools = [
            {
                "type": "function",
                "function": {
                    "name": action.name,
                    "description": action.description[:1024],
                    "parameters": action.parameters
                },
            } for action in actions
        ]
        return tools

    def construct_prompt(self,
                         actions: List[Action],
                         goals: List[Goal],
                         memory: Memory) -> Prompt:
        prompt = []
        prompt.extend(self.format_goals(goals))
        prompt.extend(self.format_memory(memory))

        tools = self.format_actions(actions)
        return Prompt(messages=prompt, tools=tools)

    def adapt_prompt_after_parsing_error(self,
                                         prompt: Prompt,
                                         response: str,
                                         traceback: str,
                                         error: Any,
                                         retries_left: int) -> Prompt:

        return prompt

    def parse_response(self, response: str | dict) -> dict:
        """Parse LLM response into structured format by extracting the ```json block"""
        try:
            if isinstance(response, str):
                return json.loads(response)
            return response
        except Exception as e:
            return {
                "tool": "terminate",
                "args": {"message": response},
                "error": str(e)
            }
