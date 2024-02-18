from typing import Generator

from app.db.session import SessionLocal


def get_db() -> Generator:
    """DB接続を行うジェネレータ関数

    Yields:
        Generator: DBセッション
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
