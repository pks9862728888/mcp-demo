from typing import Callable, Dict, List, Any
from datetime import datetime, timezone

from pydantic import BaseModel


class ActionResult(BaseModel):
    tool_executed: bool
    tool_name: str
    error: str | None = None
    traceback: str | None = None
    result: Any = None
    timestamp: str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")


class Action:
    def __init__(self,
                 name: str,
                 function: Callable,
                 description: str,
                 parameters: Dict,
                 terminal: bool = False):
        self.name = name
        self.function = function
        self.description = description
        self.parameters = parameters
        self.terminal = terminal

    def execute(self, **kwargs) -> Dict:
        """Execute the action's function."""
        return self.function(**kwargs)


class ActionRegistry:
    def __init__(self):
        self.actions = {}

    def register(self, action: Action):
        self.actions[action.name] = action

    def get(self, name: str) -> Action | None:
        return self.actions.get(name, None)

    def list_actions(self) -> List[Action]:
        return list(self.actions.values())
