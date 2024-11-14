from typing import List, Optional

from pydantic import BaseModel

from enums.tasks import TaskStatus


class BaseTasksSchema(BaseModel):
    task_name: str
    task_descriptions: str
    status: TaskStatus


class CreateTasksSchema(BaseTasksSchema):
    creator_id: int


class CreateTasksResponseSchema(BaseTasksSchema):
    id: int


class GetTaskResponseSchema(BaseTasksSchema):
    id: int


class GetTasksResponseSchema(BaseModel):
    tasks: List[GetTaskResponseSchema]


class GetUerTasksResponseSchema(BaseModel):
    tasks: List[BaseTasksSchema]


class SubscribeOnTasksSchema(BaseModel):
    user_id: int
    task_id: int


class TaskUpdateRequestSchema(BaseModel):
    task_name: Optional[str] = None
    task_descriptions: Optional[str] = None

    class Config:
        from_attributes = True


class ChangeTaskStatusSchema(BaseModel):
    status: TaskStatus
