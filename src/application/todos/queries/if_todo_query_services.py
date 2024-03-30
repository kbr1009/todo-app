from abc import ABC, abstractmethod
from typing import List

from src.application.todos.queries.todo_data_responses import TodoDataResponse


class IGetTodoByTodoIdQuery(ABC):
    @abstractmethod
    def execute(self, todo_id: str) -> TodoDataResponse:
        raise NotImplementedError()


class IGetAllTodoByUserIdQuery(ABC):
    @abstractmethod
    def execute(self, user_id: str) -> List[TodoDataResponse]:
        raise NotImplementedError()
