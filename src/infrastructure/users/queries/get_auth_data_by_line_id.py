import pyodbc
from src.application.users.queries.if_get_auth_data_by_line_id import IGetAuthDataByLineIdQuery
from src.application.users.queries.user_auth_data_by_line_response import UserAuthDataByLineResponse


class GetAuthDataByLineIdQuery(IGetAuthDataByLineIdQuery):
    def __init__(self, db_path):
        self.db_path = db_path

    def execute(self, line_id: str) -> UserAuthDataByLineResponse:
        sql_query = f"""
        SELECT 
            * 
        FROM
            dbo.users 
        WHERE 
            line_id = ?
        """

        with pyodbc.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query, (line_id,))
            row = cursor.fetchone()

        if row:
            return UserAuthDataByLineResponse(id=row.id,
                                              line_id=row.line_id,
                                              user_name=row.username,
                                              email=row.email,
                                              hashed_password=row.hashed_password)
