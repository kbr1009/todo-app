from datetime import datetime
from sqlalchemy import (
    UnicodeText,
    NVARCHAR,
    ForeignKey,
    DateTime,
    Table,
    Column,
    Boolean,
    Integer
)
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
    declarative_base
)

Base = declarative_base()


# 中間テーブルの定義
todo_category_association_table = Table('todo_category_association', Base.metadata,
    Column('todo_id', NVARCHAR(36), ForeignKey('todos.id'), primary_key=True),
    Column('category_id', NVARCHAR(36), ForeignKey('categories.id'), primary_key=True)
)


class UserDBModel(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(NVARCHAR(36), primary_key=True)
    line_id: Mapped[str] = mapped_column(NVARCHAR(100), nullable=True)
    username: Mapped[str] = mapped_column(NVARCHAR(100))
    email: Mapped[str] = mapped_column(NVARCHAR(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(NVARCHAR(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    todos: Mapped[list["TodoDBModel"]] = relationship("TodoDBModel", back_populates="user")
    categories: Mapped[list["CategoryDBModel"]] = relationship("CategoryDBModel", back_populates="user")


class CategoryDBModel(Base):
    __tablename__ = "categories"
    id: Mapped[str] = mapped_column(NVARCHAR(36), primary_key=True)
    name: Mapped[str] = mapped_column(NVARCHAR(100))
    user_id: Mapped[str] = mapped_column(NVARCHAR(36), ForeignKey("users.id"))
    tag_color: Mapped[str] = mapped_column(NVARCHAR(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped["UserDBModel"] = relationship("UserDBModel", back_populates="categories")
    todos: Mapped[list["TodoDBModel"]] = relationship(
        "TodoDBModel", secondary=todo_category_association_table, back_populates="categories")


class TodoDBModel(Base):
    __tablename__ = "todos"
    id: Mapped[str] = mapped_column(NVARCHAR(36), primary_key=True)
    title: Mapped[str] = mapped_column(NVARCHAR(100))
    details: Mapped[str] = mapped_column(UnicodeText, nullable=True)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    # notify_days_before: Mapped[int] = Column(Integer, nullable=True)
    user_id: Mapped[str] = mapped_column(NVARCHAR(36), ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["UserDBModel"] = relationship("UserDBModel", back_populates="todos")
    categories: Mapped[list["CategoryDBModel"]] = relationship(
        "CategoryDBModel", secondary=todo_category_association_table, back_populates="todos")
