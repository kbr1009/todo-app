from src.domain.users.user_value_objects import UserName

username: UserName = UserName("aaaa")
print(username.value)

username2: UserName = UserName.create_user_name_by_line("小林怜雄")
print(username2.value)

