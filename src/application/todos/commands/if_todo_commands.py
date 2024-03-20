from abc import ABC, abstractmethod
from src.application.todos.commands.todo_requests import *


class ICreateNewTodoCommand(ABC):
    @abstractmethod
    def execute(self, request: CreateNewTodoRequest) -> None:
        raise NotImplementedError()


class IAmendTodoCommand(ABC):

    @abstractmethod
    def execute(self, request: AmendTodoRequest) -> None:
        raise NotImplementedError()


class ICompleteTodoCommand(ABC):

    @abstractmethod
    def execute(self, request: CompleteTodoRequest) -> None:
        raise NotImplementedError()


class IDeleteTodoCommand(ABC):

    @abstractmethod
    def execute(self, request: DeleteTodoRequest) -> None:
        raise NotImplementedError()


