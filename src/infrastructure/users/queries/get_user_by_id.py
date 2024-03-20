import pyodbc

from src.application.users.queries.if_get_user_by_id import IGetUserQuery
from src.application.users.queries.user_data_response import UserDataResponse


class GetUserQuery(IGetUserQuery):
    def __init__(self, db_path):
        self.db_path = db_path

    def execute(self, user_id: str) -> UserDataResponse:
        sql_query = """
        SELECT 
            * 
        FROM
            dbo.users 
        WHERE 
            id = ?
        """

        with pyodbc.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query, (user_id,))
            row = cursor.fetchone()

        if row:
            return UserDataResponse(id=row.id,
                                    user_name=row.username,
                                    email=row.email,
                                    hashed_password=row.hashed_password,
                                    created=row.created_at,
                                    is_active=row.is_active)
