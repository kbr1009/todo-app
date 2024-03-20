import pyodbc
import re
from src.application.users.queries.if_get_auth_data_by_email_and_pass import IGetAuthDataQuery
from src.application.users.queries.user_auth_data_response import UserAuthDataResponse


class GetAuthDataQuery(IGetAuthDataQuery):
    def __init__(self, db_path):
        self.db_path = db_path

    def execute(self, upn: str, hashed_password: str) -> UserAuthDataResponse:
        # upnはメールアドレスかユーザ名が入力される、それによりSQLの検索条件が変化する
        email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        is_email: bool = email_pattern.match(upn) is not None
        field_name: str = 'email' if is_email else 'username'

        sql_query = f"""
        SELECT 
            * 
        FROM
            dbo.users 
        WHERE 
            {field_name} = ?
        AND 
            hashed_password = ?
        """

        with pyodbc.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query, (upn, hashed_password,))
            row = cursor.fetchone()

        if row:
            return UserAuthDataResponse(id=row.id,
                                        user_name=row.username,
                                        email=row.email,
                                        hashed_password=row.hashed_password)
