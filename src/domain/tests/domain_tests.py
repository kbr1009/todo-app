import re
import uuid

from src.domain.users.user import *
from src.domain.users.user_domain_exception import UserDomainException


# user_id: UserId = UserId.create()
# print(type(user_id))
# print(user_id)
#
# try:
#     email_address: EmailAddress = EmailAddress("@..com")
#     print("OK!")
#     print(email_address.value)
# except UserDomainException as e:
#     print("Failed!")
#     print(e)
# except Exception as e:
#     print("Failed!")
#     print(e)
#
# upn: str = "reo@koba.com"
# email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
# is_email: bool = email_pattern.match(upn) is not None
# print(is_email)
# print(type(is_email))
# field_name = 'email' if is_email else 'username'
# print(field_name)

try:
    user: User = User.create_new_user(UserName("aa"), Password("aaa"), EmailAddress("bbb@bbb.com"))
    user.user_id = UserId.create()
    print(user.user_id.value)
except UserDomainException as e:
    print(e)


