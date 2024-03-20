from src.domain.users.if_user_repository import IUserRepository
from src.domain.users.user import User


class UserDomainService:
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    def is_duplicated_user_by_email_address(self, user: User) -> bool:
        """
        指定されたemail addressが重複しているかどうかをチェックします。
        :param user: チェックするユーザーオブジェクト
        :return: ユーザーが重複していればTrue、そうでなければFalse
        """
        return self._user_repository.find_by_email_address(user.email_address.value) is not None
