from dataclasses import dataclass


@dataclass
class UserAuthDataResponse:
    id: str
    user_name: str
    email: str
    hashed_password: str
