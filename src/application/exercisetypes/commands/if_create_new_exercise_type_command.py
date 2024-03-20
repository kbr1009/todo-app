from abc import ABC, abstractmethod
from src.application.exercisetypes.commands.create_new_exercise_request import *


class ICreateNewExerciseCommand(ABC):
    @abstractmethod
    def execute(self, request: CreateNewExerciseTypeRequest) -> None:
        raise NotImplementedError()