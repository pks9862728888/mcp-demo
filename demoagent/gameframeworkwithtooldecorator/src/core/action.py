from typing import Callable, Dict, List, Any
from datetime import datetime, timezone
from src.core.tool import global_tool_registry

from pydantic import BaseModel


class ActionResult(BaseModel):
    tool_executed: bool = False
    tool_name: str | None = None
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

    def list_action_names(self) -> List[str]:
        return list(self.actions.keys())


class PythonActionRegistry(ActionRegistry):
    def __init__(self, tags: List[str] | None = None,
                 tool_names: List[str] | None = None):
        super().__init__()
        self.terminate_tool = None

        for tool_name, tool_desc in global_tool_registry.tools.items():
            if tool_name == "terminate":
                self.terminate_tool = tool_desc

            if tool_names and tool_name not in tool_names:
                continue

            tool_tags = tool_desc.get("tags", [])
            if tags and not any(tag in tool_tags for tag in tags):
                continue

            self.register(Action(
                name=tool_name,
                function=tool_desc["function"],
                description=tool_desc["description"],
                parameters=tool_desc["parameters"],
                terminal=tool_desc["terminal"]
            ))
        self.register_terminate_tool()

    def register_terminate_tool(self) -> None:
        if self.terminate_tool:
            self.register(Action(
                name="terminate",
                function=self.terminate_tool["function"],
                description=self.terminate_tool["description"],
                parameters=self.terminate_tool.get("parameters", {}),
                terminal=self.terminate_tool.get("terminal", False)
            ))
        else:
            raise Exception("Terminate tool not found in tool registry")
