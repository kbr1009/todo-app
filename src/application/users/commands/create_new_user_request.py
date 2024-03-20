from dataclasses import dataclass


@dataclass
class CreateNewUserRequest:
    user_name: str
    mail_address: str
    password: str
