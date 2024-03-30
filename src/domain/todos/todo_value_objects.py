from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from dataclasses import dataclass, field
from src.domain.shard.identity import Identity
from src.domain.shard.value_object import ValueObject


@dataclass(frozen=True)
class TodoId(Identity):
    pass


@dataclass(frozen=True)
class TodoTitle(ValueObject):
    value: str


# @dataclass(frozen=True)
# class DueDate:
#     value: Optional[datetime] = field(default=None)
#     timezone: str = field(default='Asia/Tokyo')  # タイムゾーンを動的に指定
#
#     def __post_init__(self):
#         # タイムゾーンの設定をensure_timezoneメソッドへ移動
#         object.__setattr__(self, 'value', self.ensure_timezone(self.value, self.timezone))
#
#         now_with_timezone = datetime.now(ZoneInfo(self.timezone))
#         if self.value is not None and self.value < now_with_timezone:
#             raise ValueError("期日は現在時刻より前に設定することはできません。")
#
#     @staticmethod
#     def ensure_timezone(value: Optional[datetime], timezone_str: str) -> Optional[datetime]:
#         if value is not None and (value.tzinfo is None or value.tzinfo.utcoffset(value) is None):
#             return value.replace(tzinfo=ZoneInfo(timezone_str))
#         return value


@dataclass(frozen=True)
class DueDate:
    value: Optional[datetime] = field(default=None)
    registration_date: Optional[datetime] = field(default=None)
    timezone: str = field(default='Asia/Tokyo')

    def __post_init__(self):
        # タイムゾーンの設定をensure_timezoneメソッドへ移動
        object.__setattr__(self, 'value', self.ensure_timezone(self.value, self.timezone))
        object.__setattr__(self, 'registration_date', self.ensure_timezone(self.registration_date, self.timezone))

        # 期日と登録日の比較
        if self.value is not None and self.value < self.registration_date:
            raise ValueError("期日は登録日より前に設定することはできません。")

    @staticmethod
    def ensure_timezone(value: Optional[datetime], timezone_str: str) -> Optional[datetime]:
        if value is not None and (value.tzinfo is None or value.tzinfo.utcoffset(value) is None):
            return value.replace(tzinfo=ZoneInfo(timezone_str))
        return value
