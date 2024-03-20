import os
from sqlalchemy import create_engine
from src.infrastructure.sqlserver.models import Base


# pyodbcの接続文字列
DB_DRIVER = 'ODBC Driver 17 for SQL Server'
DB_SERVER = os.environ['DB_SERVER']
DB_NAME = os.environ['DB_NAME']
DB_USER_NAME = os.environ['DB_USER_NAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
CON_STR: str = f'DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER_NAME};PWD={DB_PASSWORD}'


def execute_migrate(odbc_connect_str: str) -> None:
    # データベースに接続するエンジンを作成
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % odbc_connect_str, echo=True)
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(e)
        print("Error connecting to ")


if __name__ == '__main__':
    execute_migrate(CON_STR)
