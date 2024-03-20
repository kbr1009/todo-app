from dataclasses import dataclass
from datetime import datetime
from src.domain.exercisetypes.exercise_type_value_objects import (
    ExerciseTypeId,
    ExerciseTypeName,
    CategoryTag
)


@dataclass
class ExerciseType:
    exercise_type_id: ExerciseTypeId
    exercise_type_name: ExerciseTypeName
    category_tags: list[CategoryTag]
    user_id: str
    created_at: datetime
    is_deleted: bool = False

    @classmethod
    def create_new_exercise_type(
            cls, exercise_type_name: ExerciseTypeName,
            category_tags: list[CategoryTag], user_id: str):
        return cls(exercise_type_id=ExerciseTypeId.create(),
                   exercise_type_name=exercise_type_name,
                   category_tags=category_tags, user_id=user_id,
                   created_at=datetime.utcnow())

    def tag(self, category_tag: CategoryTag) -> None:
        self.category_tags.append(category_tag)

    def delete(self):
        self.is_deleted = True

    def change_category_name(self, exercise_type_name: ExerciseTypeName) -> None:
        self.category_name = exercise_type_name
