from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def create_db_section(odbc_connect_str: str) -> sessionmaker[Session]:
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % odbc_connect_str, echo=True)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

