from typing import Optional, List
from sqlalchemy.orm import Session
from src.domain.todos.if_todo_repository import ITodoRepository
from src.domain.todos.todo import Todo
from src.domain.todos.todo_value_objects import *
from src.infrastructure.sqlserver.models import *


class TodoRepository(ITodoRepository):
    def __init__(self, db_context: Session):
        self.db_context = db_context

    def create_new_todo(self, todo: Todo) -> None:
        """
        todoを新たに作成します。
        """
        todo_db = TodoDBModel(
            id=str(todo.todo_id.value),
            title=todo.todo_title.value,
            details=todo.todo_details,
            due_date=todo.due_date.value if todo.due_date else None,
            is_completed=todo.is_completed,
            user_id=todo.user_id,
        )

        # CategoryDBModelインスタンスを検索してTodoDBModelに関連付ける
        if todo.tag_ids:
            categories = (self.db_context.query(CategoryDBModel)
                          .filter(CategoryDBModel.id.in_(todo.tag_ids))
                          .all())
            todo_db.categories = categories

        # 変更をデータベースに反映
        self.db_context.add(todo_db)
        self.db_context.commit()

    def update_todo(self, todo: Todo) -> None:
        """
        todoを編集します。
        """
        pass

    def complete_todo(self, todo_id: str) -> None:
        """
        todo_idをキーにTODOの完了ステータスをTrueにします。
        """
        todo = (self.db_context.query(TodoDBModel)
                .filter(TodoDBModel.id == todo_id)
                .first())
        if todo:
            todo.is_completed = True
            self.db_context.commit()

    def delete_todo(self, todo_id: str) -> None:
        """
        todo_idをキーにTODOを削除します。
        """
        todo = (self.db_context.query(TodoDBModel)
                .filter(TodoDBModel.id == todo_id)
                .first())
        if todo:
            self.db_context.delete(todo)
            self.db_context.commit()

    def find_by_todo_id(self, todo_id: str) -> Optional[Todo]:
        todo_db = self.db_context.query(TodoDBModel).filter(TodoDBModel.id == todo_id).first()
        if not todo_db:
            return None  # Todoが見つからない場合はNoneを返す

        # TodoDBModelからTodoドメインオブジェクトへの変換
        todo = Todo(
            todo_id=TodoId(todo_db.id),
            user_id=todo_db.user_id,
            todo_title=TodoTitle(todo_db.title),
            due_date=None if not todo_db.due_date else DueDate(todo_db.due_date),
            todo_details=todo_db.details,
            is_completed=todo_db.is_completed,
            is_deleted=todo_db.is_deleted,
            tag_ids=[category.id for category in todo_db.categories]  # カテゴリのIDリストを抽出
        )
        return todo

    def count_categories_by_ids(self, category_ids: List[str]) -> int:
        """
        指定されたカテゴリIDのリストに基づいて、存在するカテゴリの数を返します。
        :param category_ids: チェックするカテゴリIDのリスト
        :return: 存在するカテゴリの数
        """
        count = (self.db_context.query(CategoryDBModel)
                 .filter(CategoryDBModel.id.in_(category_ids))
                 .count())
        return count

