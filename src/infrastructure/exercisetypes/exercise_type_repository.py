from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.infrastructure.sqlserver.models import MyExerciseTypesDBModel
from src.domain.exercisetypes.exercise_type import ExerciseType
from src.domain.exercisetypes.if_exercise_type_repository import IExerciseTypeRepository


class ExerciseTypeRepository(IExerciseTypeRepository):
    def __init__(self, db_context: Session):
        self.db_context = db_context

    def find_by_id(self, exercise_type_id: str) -> Optional[ExerciseType]:
        raise NotImplementedError()

    def find_by_exercise_type_name(self, exercise_type_name: str) -> Optional[ExerciseType]:
        return self.db_context.execute(
            select(MyExerciseTypesDBModel)
            .where(
                MyExerciseTypesDBModel.exercise_name == exercise_type_name
            )
        ).scalars().first()

    def save(self, exercise_type: ExerciseType) -> None:
        db_new_exercise_type = MyExerciseTypesDBModel(
            id=exercise_type.exercise_type_id.value,
            exercise_name=exercise_type.exercise_type_name.value,
            created_at=exercise_type.created_at,
            owner_id=exercise_type.user_id,
            is_deleted=exercise_type.is_deleted
        )

    def update(self, exercise_type: ExerciseType) -> None:
        raise NotImplementedError()
