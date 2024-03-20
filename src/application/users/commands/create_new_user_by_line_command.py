from src.application.users.commands.create_new_user_by_line_request import CreateNewUserByLineRequest
from src.application.users.commands.if_create_new_user_by_line_command import ICreateNewUserByLineCommand
from src.domain.users.if_user_repository import IUserRepository
from src.domain.users.user import User
from src.domain.users.user_value_objects import *


class CreateNewUserByLineCommand(ICreateNewUserByLineCommand):
    def __init__(self, repository: IUserRepository):
        self._repository = repository

    def execute(self, request: CreateNewUserByLineRequest) -> None:
        try:
            new_user: User = User.create_new_user_by_line(
                line_id=request.line_id,
                user_name=UserName.create_user_name_by_line(request.user_name),
                email_address=EmailAddress(request.mail_address))
        except Exception as e:
            print("ドメインでのエラー", e)
            raise Exception(e)

        try:
            self._repository.save_user_by_line(new_user)
        except Exception as e:
            print("SQLでのエラー", e)
            raise Exception(e)
