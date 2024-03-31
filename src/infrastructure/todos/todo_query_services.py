from sqlalchemy import case
from sqlalchemy.orm import Session
from src.infrastructure.sqlserver.models import TodoDBModel
from src.application.todos.queries.if_todo_query_services import *
from src.application.todos.queries.todo_data_responses import *


class GetTodoByTodoIdQuery(IGetTodoByTodoIdQuery):
    def __init__(self, db_context: Session):
        self.db_context = db_context

    def execute(self, todo_id: str) -> Optional[TodoDataResponse]:
        todo = (self.db_context.query(TodoDBModel)
                .filter(TodoDBModel.id == todo_id).first())
        if todo:
            return TodoDataResponse(
                todo_id=todo.id,
                todo_title=todo.title,
                is_completed=todo.is_completed,
                registration_date=todo.created_at,
                todo_details=todo.details,
                due_date=todo.due_date,
                completed_date=todo.completed_at,
                tags=[TagDataResponse(tag_id=category.id,
                                      tag_name=category.name)
                      for category in todo.categories])
        return None


class GetAllTodoByUserIdQuery(IGetAllTodoByUserIdQuery):
    def __init__(self, db_context: Session):
        self.db_context = db_context

    def execute(self, user_id: str) -> List[TodoDataResponse]:
        todos = (self.db_context.query(TodoDBModel)
                 .filter(TodoDBModel.user_id == user_id)
                 .order_by(case((TodoDBModel.due_date.is_(None), 1), else_=0),
                           TodoDBModel.due_date)
                 .all())
        return [TodoDataResponse(todo_id=todo.id,
                                 todo_title=todo.title,
                                 is_completed=todo.is_completed,
                                 registration_date=todo.created_at,
                                 todo_details=todo.details,
                                 due_date=todo.due_date,
                                 completed_date=todo.completed_at,
                                 tags=[TagDataResponse(tag_id=category.id,
                                                       tag_name=category.name)
                                       for category in todo.categories]) for todo in todos]
