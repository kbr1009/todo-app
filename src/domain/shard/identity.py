import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class Identity:
    value: str

    @classmethod
    def create(cls):
        new_uuid = uuid.uuid4()
        return cls(str(new_uuid))
