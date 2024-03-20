from abc import ABC, abstractmethod
from src.application.users.commands.create_new_user_request import *


class ICreateNewUserCommand(ABC):
    @abstractmethod
    def execute(self, request: CreateNewUserRequest) -> None:
        raise NotImplementedError()
