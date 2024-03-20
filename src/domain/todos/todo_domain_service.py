from src.domain.todos.if_todo_repository import ITodoRepository
from src.domain.todos.todo import Todo


class TodoDomainService:
    def __init__(self, todo_repository: ITodoRepository):
        self._todo_repository = todo_repository

    def is_category_exist(self, domain_obj: Todo) -> bool:
        """
        Todoオブジェクトにあるtag_idsで指定されたタグがDBに存在しているかどうかをチェックします。
        :param domain_obj: チェックするTodoオブジェクト
        :return: tag_idsが全て存在していればTrue、そうでなければFalse
        """
        if not domain_obj.tag_ids:
            # tag_idsが空の場合はチェック不要
            return True

        # データベースからtag_idsに対応するカテゴリの数を取得
        categories_count = self._todo_repository.count_categories_by_ids(domain_obj.tag_ids)

        # tag_idsの数とデータベースから取得したカテゴリの数が一致するかチェック
        return categories_count == len(domain_obj.tag_ids)

    def is_duplicated_user_by_username(self, domain_obj: Todo) -> bool:
        """
        指定されたユーザー名が重複しているかどうかをチェックします。
        :param domain_obj: チェックするユーザーオブジェクト
        :return: ユーザーが重複していればTrue、そうでなければFalse
        """
        raise NotImplemented()