from typing import List
from core.action import Action
from core.environment import Environment
from core.goal import Goal
from core.memory import Memory
from core.prompt import Prompt


class AgentLanguage:
    def __init__(self):
        pass

    def construct_prompt(self,
                         actions: List[Action],
                         environment: Environment,
                         goals: List[Goal],
                         memory: Memory) -> Prompt:
        raise NotImplementedError("construct_prompt not implemented.")

    def parse_response(self, response: dict) -> dict:
        raise NotImplementedError("parse_response not implemented.")
