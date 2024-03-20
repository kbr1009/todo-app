from abc import ABC, abstractmethod
from src.application.users.queries.user_auth_data_by_line_response import UserAuthDataByLineResponse


class IGetAuthDataByLineIdQuery(ABC):
    @abstractmethod
    def execute(self, line_id: str) -> UserAuthDataByLineResponse:
        raise NotImplementedError()
