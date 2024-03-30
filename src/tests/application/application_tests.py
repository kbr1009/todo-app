from src.app.setup import DIModule
from injector import Injector

from src.application.todos.commands.todo_commands import *
from src.application.todos.commands.todo_requests import *
from src.application.todos.queries.if_todo_query_services import *
from src.application.users.queries.if_get_user_by_id import IGetUserQuery
from src.application.users.queries.user_data_response import UserDataResponse


def main():
    # テストデータ
    user_id: str = "77922516-837a-4f24-a3b3-b3adb6aa0ad7"
    todo_title: str = "VPNを設定する"
    todo_details: str = "業務PCのVPNの設定を更新する"

    # ユーザ取得の実行
    injector = Injector([DIModule()])
    user_query: IGetUserQuery = injector.get(IGetUserQuery)
    user_data_response: UserDataResponse = user_query.execute(user_id=user_id)

    create_todo_req: CreateNewTodoRequest = CreateNewTodoRequest(user_id=user_data_response.id,
                                                                 todo_title=todo_title,
                                                                 todo_details=todo_details)
    # Todo登録の実行
    create_todo_command: ICreateNewTodoCommand = injector.get(ICreateNewTodoCommand)
    try:
        create_todo_command.execute(create_todo_req)
    except Exception as e:
        print(e)

    # Todo取得の実行
    get_all_todo_query: IGetAllTodoByUserIdQuery = injector.get(IGetAllTodoByUserIdQuery)
    try:
        print(f"'{user_data_response.user_name}' の全てのTodoデータを取得します。")
        todo_list: List[TodoDataResponse] = get_all_todo_query.execute(user_id=user_data_response.id)
        if not len(todo_list) == 0:
            todo: TodoDataResponse = todo_list[0]

            print(f"'{user_data_response.user_name}' の全てのTodoリストデータは以下")
            for todo_data in todo_list:
                print(todo_data)

            # todo_idでのTodoの検索
            get_todo_query: IGetTodoByTodoIdQuery = injector.get(IGetTodoByTodoIdQuery)
            try:
                print(f"'{todo.todo_title}' のTodoデータを取得します。")
                get_todo_by_todo_id: TodoDataResponse = get_todo_query.execute(todo_id=todo.todo_id)
                if get_todo_by_todo_id:
                    print(f"'{todo.todo_title}' Todoデータは以下")
                    print(get_todo_by_todo_id)

            except Exception as e:
                print(f"'{todo.todo_title}' のTodoデータ取得に失敗した。")
                print(e)

    except Exception as e:
        print(f"'{user_data_response.user_name}' の全てのTodoデータの取得に失敗しました。")
        print(e)


if __name__ == "__main__":
    main()
