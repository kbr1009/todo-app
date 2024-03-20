import os
from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from injector import Injector, Module
from routers import configure_routing
from src.application.todos.commands.todo_commands import *
from src.application.users.commands.create_new_user_by_line_command import CreateNewUserByLineCommand
from src.application.users.commands.create_new_user_command import CreateNewUserCommand
from src.application.users.commands.if_create_new_user_by_line_command import ICreateNewUserByLineCommand
from src.application.users.commands.if_create_new_user_command import ICreateNewUserCommand
from src.application.users.queries.if_get_auth_data_by_email_and_pass import IGetAuthDataQuery
from src.application.users.queries.if_get_auth_data_by_line_id import IGetAuthDataByLineIdQuery
from src.application.users.queries.if_get_user_by_id import IGetUserQuery
from src.domain.todos.if_todo_repository import ITodoRepository
from src.domain.users.if_user_repository import IUserRepository
from src.infrastructure.todos.queries.todo_repository import TodoRepository
from src.infrastructure.users.queries.get_auth_data_by_line_id import GetAuthDataByLineIdQuery
from src.infrastructure.users.queries.get_auth_data_by_upn_and_pass import GetAuthDataQuery
from src.infrastructure.users.queries.get_user_by_id import GetUserQuery
from src.infrastructure.sqlserver.settings import create_db_section
from src.infrastructure.users.user_repository import UserRepository

# 環境変数
# DB
DB_SERVER = os.environ['DB_SERVER']
DB_NAME = os.environ['DB_NAME']
DB_USER_NAME = os.environ['DB_USER_NAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
# LINE
LINE_CHANNEL_ID = os.environ['LINE_CHANNEL_ID']
LINE_CLIENT_SECRET = os.environ['LINE_CLIENT_SECRET']
LINE_REDIRECT_URI = os.environ['LINE_REDIRECT_URI']

# DBコネクション情報
connection_string: str = f'DRIVER={{SQL Server}};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER_NAME};PWD={DB_PASSWORD}'
Session = create_db_section(connection_string)


class DIModule(Module):
    def configure(self, binder) -> None:

        # ここで依存関係を設定
        # UserのDI
        binder.bind(IGetUserQuery, to=GetUserQuery(db_path=connection_string))
        binder.bind(IGetAuthDataQuery, to=GetAuthDataQuery(db_path=connection_string))
        binder.bind(IGetAuthDataByLineIdQuery, to=GetAuthDataByLineIdQuery(db_path=connection_string))
        binder.bind(IUserRepository, to=UserRepository(db_context=Session()))
        user_repo = binder.injector.get(IUserRepository, scope=None)
        binder.bind(ICreateNewUserCommand, to=CreateNewUserCommand(user_repo))
        binder.bind(ICreateNewUserByLineCommand, to=CreateNewUserByLineCommand(user_repo))

        # TodoのDI
        binder.bind(ITodoRepository, to=TodoRepository(db_context=Session()))
        todo_repo = binder.injector.get(ITodoRepository, scope=None)
        binder.bind(ICreateNewTodoCommand, to=CreateNewTodoCommand(todo_repo))
        binder.bind(IAmendTodoCommand, to=AmendTodoCommand(todo_repo))
        binder.bind(ICompleteTodoCommand, to=CompleteTodoCommand(todo_repo))
        binder.bind(IDeleteTodoCommand, to=DeleteTodoCommand(todo_repo))

        # TODO: TagのDI


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = os.environ['FLASK_SECRET_KEY']

    login_manager = LoginManager()
    login_manager.init_app(app)

    with app.app_context():
        injector = Injector([DIModule()])
        configure_routing(app, login_manager, injector)

    # CSRF対策
    CSRFProtect(app)
    return app


def main() -> None:
    app = create_app()
    # デバッグモードを環境変数から設定
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() in ['true', '1', 't']
    app.debug = debug_mode
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()

