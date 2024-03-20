from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CreateNewTodoRequest:
    """
    Todoを新規作成する際のリクエストオブジェクト
    """
    user_id: str
    todo_title: str
    todo_details: str
    due_date: datetime
    tags: Optional[List[str]] = field(default_factory=list)


@dataclass
class AmendTodoRequest:
    """
    Todoを編集する際のリクエストオブジェクト
    """
    todo_id: str
    todo_title: str
    todo_details: str
    due_date: datetime
    tag_ids: Optional[List[str]] = field(default_factory=list)


@dataclass
class CompleteTodoRequest:
    """
    Todoを完了させる際のリクエストオブジェクト
    """
    todo_id: str


@dataclass
class DeleteTodoRequest:
    """
    Todoを削除する際のリクエストオブジェクト
    """
    todo_id: str
