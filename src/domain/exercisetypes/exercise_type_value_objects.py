from dataclasses import dataclass
from datetime import datetime
from src.domain.shard.identity import Identity
from src.domain.shard.value_object import ValueObject
from src.domain.shard.domain_exception import DomainException


@dataclass(frozen=True)
class ExerciseTypeId(Identity):
    pass


@dataclass(frozen=True)
class ExerciseTypeName(ValueObject):
    value: str

    def __post_init__(self):
        if not self._is_valid_exercise_type_name_(self.value):
            raise DomainException(f"種目名の形式が不正です: {self.value}")

    @staticmethod
    def _is_valid_exercise_type_name_(exercise_type_name: str) -> bool:
        return True


@dataclass(frozen=True)
class CategoryTag:
    category_tag_name: str
    created_at: datetime = datetime.utcnow()

    def __post_init__(self):
        if not self._is_valid_exercise_type_name_(self.category_tag_name):
            raise DomainException(f"タグ名の形式が不正です: {self.category_tag_name}")

    @staticmethod
    def _is_valid_exercise_type_name_(exercise_type_name: str) -> bool:
        return True
