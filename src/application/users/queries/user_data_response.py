from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserDataResponse:
    id: str
    user_name: str
    email: str
    hashed_password: str
    created: datetime
    is_active: bool
