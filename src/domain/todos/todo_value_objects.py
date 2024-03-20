from datetime import datetime
from zoneinfo import ZoneInfo
from dataclasses import dataclass
from src.domain.shard.identity import Identity
from src.domain.shard.value_object import ValueObject


@dataclass(frozen=True)
class TodoId(Identity):
    pass


@dataclass(frozen=True)
class TodoTitle(ValueObject):
    value: str


@dataclass(frozen=True)
class DueDate(ValueObject):
    value: datetime

    def __post_init__(self):
        if self.value < datetime.now(ZoneInfo('Asia/Tokyo')):
            raise ValueError("期日は現在時刻より前に設定することはできません。")

