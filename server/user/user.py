from dataclasses import dataclass
from datetime import datetime
from bson import ObjectId
# from task.task import Task

@dataclass(frozen=True)
class User:
    _id: ObjectId
    email: str
    password: str
    # todos: list[Task] = []
    creation_date: datetime = datetime.now()
