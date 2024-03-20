import hashlib
from flask_login import UserMixin


class LoginUser(UserMixin):
    """
    flask_loginを使用するための実装
    UserMixinクラスを継承する
    """
    def __init__(self, user_id: str, user_name: str):
        self.id = user_id
        self.user_name = user_name


class PasswordService:
    """
    パスワードをハッシュ化するサービスクラス
    これはアプリケーションサービス層に書くものなのか？
    """
    def __init__(self, password: str):
        self.password = password

    def password_hash_it(self) -> str:
        hash_sha256 = hashlib.sha256(self.password.encode())
        return hash_sha256.hexdigest()

    def passwords_match(self, hashed_password: str) -> bool:
        return hashed_password == self.password_hash_it()