from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional
from src.domain.users.user_value_objects import (
    UserId,
    UserName,
    Password,
    EmailAddress,
)


@dataclass
class User:
    user_id: UserId
    user_name: UserName
    email_address: EmailAddress
    created_at: datetime
    is_active: bool = False
    is_deleted: bool = False
    password: Optional[Password] = None
    line_id: str = ""

    @classmethod
    def create_new_user(
            cls, user_name: UserName,
            password: Password,
            email_address: EmailAddress):

        return cls(
            user_id=UserId.create(),
            user_name=user_name,
            password=password,
            email_address=email_address,
            created_at=datetime.now(ZoneInfo('Asia/Tokyo')),
            is_active=False,
            is_deleted=False)

    @classmethod
    def create_new_user_by_line(
            cls, user_name: UserName,
            line_id: str,
            email_address: EmailAddress):

        return cls(
            user_id=UserId.create(),
            line_id=line_id,
            user_name=user_name,
            email_address=email_address,
            created_at=datetime.now(ZoneInfo('Asia/Tokyo')),
            is_active=False,
            is_deleted=False)

    def withdraw_from_the_service(self) -> None:
        self.is_active = False
        self.is_deleted = True
