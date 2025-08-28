import traceback
from typing import Dict
from src.core.action import Action, ActionResult


class Environment:
    def __init__(self):
        pass

    def execute_action(self, action: Action, args: Dict) -> ActionResult:
        """Execute an action within the environment."""
        try:
            result = action.execute(**args)
            return ActionResult(
                tool_executed=True,
                tool_name=action.name,
                result=result
            )
        except Exception as e:
            return ActionResult(
                tool_executed=False,
                tool_name=action.name,
                error=str(e),
                traceback=traceback.format_exc()
            )
