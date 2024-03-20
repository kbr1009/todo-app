from abc import ABC, abstractmethod
from src.application.users.queries.user_auth_data_response import UserAuthDataResponse


class IGetAuthDataQuery(ABC):
    @abstractmethod
    def execute(self, upn: str, hashed_password: str) -> UserAuthDataResponse:
        raise NotImplementedError()
