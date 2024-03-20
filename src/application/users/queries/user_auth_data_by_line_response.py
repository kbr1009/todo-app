from dataclasses import dataclass


@dataclass
class UserAuthDataByLineResponse:
    id: str
    line_id: str
    user_name: str
    email: str
    hashed_password: str
