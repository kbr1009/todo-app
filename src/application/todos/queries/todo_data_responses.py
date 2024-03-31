from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from src.application.tags.queries.tag_data_responses import TagDataResponse


@dataclass
class TodoDataResponse:
    todo_id: str
    todo_title: str
    is_completed: bool
    registration_date: datetime
    todo_details: Optional[str] = None
    due_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    tags: Optional[List[TagDataResponse]] = field(default_factory=list)

