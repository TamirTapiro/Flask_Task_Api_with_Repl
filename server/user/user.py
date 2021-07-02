from dataclasses import dataclass
from datetime import datetime
from bson import ObjectId
# from task.task import Task

@dataclass
class User:
    email: str
    password: str
    _id: ObjectId = ObjectId
    creation_date: datetime = datetime.now()

    def __post_init__(self):
        self._id = ObjectId()
