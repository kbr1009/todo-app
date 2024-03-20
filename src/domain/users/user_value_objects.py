import re
from dataclasses import dataclass, field
from src.domain.shard.identity import Identity
from src.domain.shard.value_object import ValueObject
from src.domain.shard.domain_exception import DomainException


@dataclass(frozen=True)
class UserId(Identity):
    pass


@dataclass(frozen=True)
class UserName:
    value: str
    _skip_validation: bool = field(default=False, repr=False, compare=False, init=False)

    def __post_init__(self):
        if not self._skip_validation:
            if not self._is_valid_username(self.value):
                raise DomainException(f"ユーザ名の形式が不正です: {self.value}")

    @classmethod
    def create_user_name_by_line(cls, user_name: str):
        # _skip_validationフラグをTrueに設定してバリデーションをスキップ
        obj = cls.__new__(cls)
        object.__setattr__(obj, 'value', user_name)
        object.__setattr__(obj, '_skip_validation', True)
        return obj

    @staticmethod
    def _is_valid_username(user_name: str) -> bool:
        return re.match(r'^[a-zA-Z0-9_]+$', user_name) is not None


@dataclass(frozen=True)
class Password(ValueObject):
    value: str


@dataclass(frozen=True)
class EmailAddress(ValueObject):
    value: str

    def __post_init__(self):
        if not self._is_valid_email(self.value):
            raise DomainException(f"メールアドレスの形式が不正です: {self.value}")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) is not None
