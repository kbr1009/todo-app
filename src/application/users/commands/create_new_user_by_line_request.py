from dataclasses import dataclass


@dataclass
class CreateNewUserByLineRequest:
    line_id: str
    user_name: str
    mail_address: str
