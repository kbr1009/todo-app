from abc import ABC, abstractmethod
from src.application.users.commands.create_new_user_by_line_request import CreateNewUserByLineRequest


class ICreateNewUserByLineCommand(ABC):
    @abstractmethod
    def execute(self, request: CreateNewUserByLineRequest) -> None:
        raise NotImplementedError()