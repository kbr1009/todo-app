from abc import ABC, abstractmethod
from typing import List
from src.domain.todos.todo import Todo


class ITodoRepository(ABC):
    @abstractmethod
    def create_new_todo(self, todo: Todo) -> None:
        raise NotImplementedError()

    @abstractmethod
    def update_todo(self, todo: Todo) -> None:
        raise NotImplementedError()

    @abstractmethod
    def complete_todo(self, todo_id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_todo(self, todo_id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def find_by_todo_id(self, todo_id: str) -> Todo:
        raise NotImplementedError()

    @abstractmethod
    def count_categories_by_ids(self, category_ids: List[str]) -> int:
        """
        指定されたカテゴリIDのリストに基づいて、存在するカテゴリの数を返します。
        :param category_ids: チェックするカテゴリIDのリスト
        :return: 存在するカテゴリの数
        """
        raise NotImplementedError()
