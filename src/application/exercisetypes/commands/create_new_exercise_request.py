from dataclasses import dataclass


@dataclass
class CreateNewExerciseTypeRequest:
    exercise_type_name: str
    user_id: str
    category_tags: list[str]
