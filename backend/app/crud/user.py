from typing import List

from sqlalchemy.orm import Session

from app import (
    models,  # データベースモデルをインポート
    schemas,  # 作成したPydanticモデルをインポート
)


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """ユーザーを作成するCRUD操作

    Args:
        db (Session): データベースセッション
        user (schemas.UserCreate): 作成するユーザーの情報

    Returns:
        UserModel: 作成されたユーザーのモデル
    """
    db_user = models.User(
        **user.model_dump()
    )  # Pydanticモデルからデータベースモデルを作成
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session) -> List[models.User]:
    """ユーザーの一覧を取得するCRUD操作

    Args:
        db (Session): データベースセッション

    Returns:
        List[models.User]: 取得されたユーザーの一覧
    """
    return db.query(models.User).all()


def get_user_by_uid(db: Session, user_id: str) -> models.User:
    """ユーザーの詳細を取得するCRUD操作

    Args:
        db (Session): データベースセッション
        user_id (str): 取得するユーザーのID

    Returns:
        models.User: 取得されたユーザーの情報
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user(db: Session, user_id: str, user: schemas.UserUpdate) -> models.User:
    """ユーザーを更新するCRUD操作

    Args:
        db (Session): データベースセッション
        user_id (str): 更新するユーザーのID
        user (schemas.UserUpdate): 更新するユーザーの情報

    Returns:
        models.User: 更新されたユーザーの情報
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    for key, value in user.model_dump().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: str) -> models.User:
    """ユーザーを削除するCRUD操作

    Args:
        db (Session): データベースセッション
        user_id (str): 削除するユーザーのID

    Returns:
        models.User: 削除されたユーザーの情報
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user