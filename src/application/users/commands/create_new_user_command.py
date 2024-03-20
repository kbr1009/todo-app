from src.application.users.commands.if_create_new_user_command import ICreateNewUserCommand
from src.application.users.commands.create_new_user_request import *
from src.domain.users.if_user_repository import IUserRepository
from src.domain.users.user import User
from src.domain.users.user_value_objects import *
from src.domain.users.user_domain_service import UserDomainService


class CreateNewUserCommand(ICreateNewUserCommand):
    def __init__(self, repository: IUserRepository):
        self._repository = repository

    def execute(self, request: CreateNewUserRequest) -> None:

        is_error: bool = False
        err_msg = ""

        new_user: User = User.create_new_user(
            user_name=UserName(request.user_name),
            password=Password(request.password),
            email_address=EmailAddress(request.mail_address))

        domain_service: UserDomainService = UserDomainService(self._repository)
        if domain_service.is_duplicated_user_by_username(new_user):
            is_error = True
            err_msg.join(f"ユーザ名 '{request.user_name}' は使用することができません。他のユーザ名を入力してください。")

        if domain_service.is_duplicated_user_by_email_address(new_user):
            is_error = True
            err_msg.join(f"\nメールアドレスが '{request.mail_address}' のユーザは既に登録されているようです。")

        if is_error:
            raise DomainException(err_msg)

        self._repository.save_user(new_user)
