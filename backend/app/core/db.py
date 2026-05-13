# ./backend/app/core/db.py
from sqlmodel import SQLModel, create_engine, Session
from .config import get_settings

settings = get_settings()

# Создаем движок БД
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False}  # Для SQLite
)


def create_db_and_tables():
    """Создание всех таблиц в БД"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency для получения сессии БД"""
    with Session(engine) as session:
        yield session