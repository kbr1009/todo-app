from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from src.domain.todos.todo_value_objects import (
    TodoId,
    TodoTitle,
    DueDate
)


@dataclass
class Todo:
    todo_id: TodoId
    user_id: str
    todo_title: TodoTitle
    created_at: datetime
    due_date: Optional[DueDate] = None
    todo_details: str = ""
    is_completed: bool = False
    completed_at: datetime = None
    is_deleted: bool = False
    tag_ids: List[str] = field(default_factory=list)

    @classmethod
    def create_new_todo(
            cls, user_id: str,
            todo_title: TodoTitle,
            # オプショナルとしてNoneをデフォルト値に設定 入力ナシを許容
            due_date: Optional[DueDate] = None,
            todo_details: str = "",
            # デフォルト値としてNoneを使用 入力なしを許容
            tag_ids: List[str] = None):
        if tag_ids is None:
            tag_ids = []
        return cls(
            todo_id=TodoId.create(),
            user_id=user_id,
            todo_title=todo_title,
            created_at=datetime.now(ZoneInfo('Asia/Tokyo')),
            due_date=due_date,
            todo_details=todo_details,
            is_completed=False,
            is_deleted=False,
            tag_ids=tag_ids)

    def amend_todo(self, todo_title: TodoTitle,
                   due_date: Optional[DueDate] = None,
                   todo_details: str = "",
                   tag_ids: List[str] = None):
        if tag_ids is None:
            tag_ids = []
        self.todo_title = todo_title
        self.due_date = due_date
        self.todo_details = todo_details
        self.tag_ids = tag_ids

    def complete_todo(self):
        self.is_completed = True
        self.completed_at = datetime.now(ZoneInfo('Asia/Tokyo'))

    def undo_completion(self):
        self.is_completed = False
        self.completed_at = None
