from pydantic import BaseModel


class TaskResponse(BaseModel):
    task_type: str
    networks: str
    status: str
