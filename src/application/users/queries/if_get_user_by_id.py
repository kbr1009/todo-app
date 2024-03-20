from abc import ABC, abstractmethod
from src.application.users.queries.user_data_response import UserDataResponse


class IGetUserQuery(ABC):
    @abstractmethod
    def execute(self, user_id: str) -> UserDataResponse:
        raise NotImplementedError()
