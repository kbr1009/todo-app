from src.domain.todos.if_todo_repository import ITodoRepository
from src.application.todos.commands.if_todo_commands import *
from src.domain.todos.todo import Todo
from src.domain.todos.todo_domain_service import TodoDomainService
from src.domain.todos.todo_value_objects import *


class CreateNewTodoCommand(ICreateNewTodoCommand):
    def __init__(self, repository: ITodoRepository):
        self._repository = repository

    def execute(self, request: CreateNewTodoRequest) -> None:
        try:
            # ドメインオブジェクトの組み立て
            new_todo: Todo = Todo.create_new_todo(request.user_id,
                                                  TodoTitle(value=request.todo_title),
                                                  DueDate(value=request.due_date,
                                                          registration_date=datetime.now()),
                                                  request.todo_details, request.tags)
        except Exception as e:
            raise ValueError(f"{e}")

        # タグが存在するかチェックする
        domain_service: TodoDomainService = TodoDomainService(self._repository)
        if not domain_service.is_category_exist(new_todo):
            raise ValueError(f"存在しないタグが入力されています。")

        try:
            self._repository.create_new_todo(todo=new_todo)
        except Exception as e:
            print(e)
            raise ValueError(f"システムエラー：Todoの作成に失敗しました。")


class AmendTodoCommand(IAmendTodoCommand):
    def __init__(self, repository: ITodoRepository):
        self._repository = repository

    def execute(self, request: AmendTodoRequest) -> None:
        # idをキーにTodoを取得
        todo: Optional[Todo] = self._repository.find_by_todo_id(request.todo_id)

        # Todoが見つからない場合のエラーハンドリング
        if todo is None:
            raise ValueError(f"編集対象のTodoが見つかりません。")

        try:
            # ドメインオブジェクトの編集メソッドを使用してTodoを編集
            todo.amend_todo(TodoTitle(value=request.todo_title),
                            DueDate(value=request.due_date,
                                    registration_date=datetime.now()),
                            request.todo_details, request.tag_ids)
        except Exception as e:
            raise ValueError(f"{e}")

        # タグが存在するかチェックする
        domain_service: TodoDomainService = TodoDomainService(self._repository)
        if not domain_service.is_category_exist(todo):
            raise ValueError(f"存在しないタグが入力されています。")

        try:
            self._repository.update_todo(todo)
        except Exception as e:
            print(e)
            raise ValueError(f"システムエラー：編集したTodoの登録に失敗しました。")


class CompleteTodoCommand(ICompleteTodoCommand):
    def __init__(self, repository: ITodoRepository):
        self._repository = repository

    def execute(self, request: CompleteTodoRequest) -> None:
        """
        todo_idをキーにTodoを完了にする
        """
        # idをキーにTodoを取得
        todo: Optional[Todo] = self._repository.find_by_todo_id(request.todo_id)

        # Todoが見つからない場合のエラーハンドリング
        if todo is None:
            raise ValueError(f"完了にするTodoが見つかりません。")

        todo.complete_todo()

        try:
            # TODO:  todoオブジェクトを渡すように再実装する
            self._repository.complete_todo(todo.todo_id.value)
        except Exception as e:
            print(e)
            raise ValueError(f"システムエラー：Todoの完了処理に失敗しました。")


class DeleteTodoCommand(IDeleteTodoCommand):
    def __init__(self, repository: ITodoRepository):
        self._repository = repository

    def execute(self, request: DeleteTodoRequest) -> None:
        # idをキーにTodoを取得
        todo: Optional[Todo] = self._repository.find_by_todo_id(request.todo_id)

        # Todoが見つからない場合のエラーハンドリング
        if todo is None:
            raise ValueError(f"削除対象のTodoが見つかりません。")

        try:
            self._repository.delete_todo(todo.todo_id.value)
        except Exception as e:
            print(e)
            raise ValueError(f"システムエラー：Todoの削除処理に失敗しました。")
