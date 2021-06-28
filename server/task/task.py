from dataclasses import dataclass, field
from datetime import datetime
from bson import ObjectId


@dataclass
class Task:
    name: str
    owner: str
    _id: ObjectId = ObjectId
    completed: bool = False
    last_updated: datetime = datetime.now()
    creation_date: datetime = datetime.now()

    def __post_init__(self):
        self._id = ObjectId()
