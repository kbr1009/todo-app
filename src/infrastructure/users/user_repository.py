from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.infrastructure.sqlserver.models import UserDBModel
from src.domain.users.if_user_repository import *


class UserRepository(IUserRepository):
    def __init__(self, db_context: Session):
        self.db_context = db_context

    def find_by_id(self, user_id: str) -> Optional[User]:
        raise NotImplementedError()

    def find_by_email_address(self, email_address: str) -> Optional[User]:
        return self.db_context.execute(
            select(UserDBModel)
            .where(
                UserDBModel.email == email_address
            )
        ).scalars().first()

    def find_by_username(self, username: str) -> Optional[User]:
        return self.db_context.execute(
            select(UserDBModel)
            .where(
                UserDBModel.username == username
            )
        ).scalars().first()

    def save_user(self, user: User) -> None:
        db_new_user = UserDBModel(
            id=user.user_id.value,
            line_id="",
            username=user.user_name.value,
            email=user.email_address.value,
            hashed_password=user.password.value,
            created_at=user.created_at,
            is_active=user.is_active,
            is_deleted=user.is_deleted
        )
        try:
            self.db_context.add(db_new_user)
            self.db_context.commit()
            self.db_context.refresh(db_new_user)
        except Exception as e:
            self.db_context.rollback()
            raise e

    def save_user_by_line(self, user: User) -> None:
        db_new_user = UserDBModel(
            id=user.user_id.value,
            line_id=user.line_id,
            username=user.user_name.value,
            email=user.email_address.value,
            hashed_password="",
            created_at=user.created_at,
            is_active=user.is_active,
            is_deleted=user.is_deleted
        )
        try:
            self.db_context.add(db_new_user)
            self.db_context.commit()
            self.db_context.refresh(db_new_user)
        except Exception as e:
            self.db_context.rollback()
            raise e

    def update(self, user: User) -> None:
        raise NotImplementedError()
