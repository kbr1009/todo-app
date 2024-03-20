from abc import ABC, abstractmethod
from src.domain.exercisetypes.exercise_type import ExerciseType


class IExerciseTypeRepository(ABC):
    @abstractmethod
    def find_by_id(self, exercise_type_id: str) -> ExerciseType:
        raise NotImplementedError()

    @abstractmethod
    def find_by_exercise_type_name(self, exercise_type_name: str) -> ExerciseType:
        raise NotImplementedError()

    @abstractmethod
    def save(self, exercise_type: ExerciseType) -> None:
        raise NotImplementedError()

    @abstractmethod
    def update(self, exercise_type: ExerciseType) -> None:
        raise NotImplementedError()
