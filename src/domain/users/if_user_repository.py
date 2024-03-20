from abc import ABC, abstractmethod
from src.domain.users.user import User


class IUserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    def find_by_email_address(self, email_address: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    def find_by_username(self, username: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    def save_user(self, user: User) -> None:
        raise NotImplementedError()

    @abstractmethod
    def save_user_by_line(self, user: User) -> None:
        raise NotImplementedError()

    @abstractmethod
    def update(self, user: User) -> None:
        raise NotImplementedError()
