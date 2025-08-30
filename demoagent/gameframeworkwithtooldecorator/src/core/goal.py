from pydantic import BaseModel


class Goal(BaseModel):
    name: str
    priority: int
    description: str
