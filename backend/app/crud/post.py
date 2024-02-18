from sqlalchemy.orm import Session

from app import models, schemas


def create_post(db: Session, post: schemas.PostCreate) -> models.Post:
    """投稿を作成する関数

    Args:
        db (Session): DBセッション
        post (PostCreate): 作成する投稿の情報

    Returns:
        models.Post: 作成された投稿
    """
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session) -> list[models.Post]:
    """投稿の一覧を取得する関数

    Args:
        db (Session): DBセッション

    Returns:
        list[models.Post]: 取得された投稿の一覧
    """
    return db.query(models.Post).all()


def get_post_by_id(db: Session, post_id: str) -> models.Post:
    """投稿の詳細を取得する関数

    Args:
        db (Session): DBセッション
        post_id (str): 取得する投稿のID

    Returns:
        models.Post: 取得された投稿
    """
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def update_post(db: Session, post_id: str, post: schemas.PostCreate) -> models.Post:
    """投稿を更新する関数

    Args:
        db (Session): DBセッション
        post_id (str): 更新する投稿のID
        post (PostCreate): 更新する投稿の情報

    Returns:
        models.Post: 更新された投稿
    """
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    for key, value in post.model_dump().items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: str) -> models.Post:
    """投稿を削除する関数

    Args:
        db (Session): DBセッション
        post_id (str): 削除する投稿のID

    Returns:
        models.Post: 削除された投稿
    """
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    db.delete(db_post)
    db.commit()
    return db_post


def get_posts_by_user_id(db: Session, user_id: str) -> list[models.Post]:
    """ユーザーの投稿一覧を取得する関数

    Args:
        db (Session): DBセッション
        user_id (str): 取得するユーザーのID

    Returns:
        list[models.Post]: 取得された投稿の一覧
    """
    return db.query(models.Post).filter(models.Post.user_id == user_id).all()
