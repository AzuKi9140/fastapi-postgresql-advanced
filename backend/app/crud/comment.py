from sqlalchemy.orm import Session

from app import models, schemas


def create_comment_for_post(
    db: Session, comment: schemas.CommentCreate, post_id: str
) -> models.Comment:
    """投稿にコメントを作成する関数

    Args:
        db (Session): DBセッション
        comment (schemas.CommentCreate): 作成するコメントの情報
        post_id (str): コメントを作成する投稿のID

    Returns:
        models.Comment: 作成されたコメントの情報
    """
    db_comment = models.Comment(**comment.dict(), post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments_for_post(db: Session, post_id: str) -> list[models.Comment]:
    """投稿に対するコメントの一覧を取得する関数

    Args:
        db (Session): DBセッション
        post_id (str): 取得するコメントの投稿のID

    Returns:
        list[models.Comment]: 取得されたコメントの一覧
    """
    return db.query(models.Comment).filter(models.Comment.post_id == post_id).all()


def get_comment_by_id(db: Session, comment_id: str) -> models.Comment:
    """コメントの詳細を取得する関数

    Args:
        db (Session): DBセッション
        comment_id (str): 取得するコメントのID

    Returns:
        models.Comment: 取得されたコメント
    """
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def update_comment(
    db: Session, comment_id: str, comment: schemas.CommentUpdate
) -> models.Comment:
    """コメントを更新する関数

    Args:
        db (Session): DBセッション
        comment_id (str): 更新するコメントのID
        comment (schemas.CommentUpdate): 更新するコメントの情報

    Returns:
        models.Comment: 更新されたコメント
    """
    db_comment = (
        db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    )
    for key, value in comment.model_dump(exclude_unset=True).items():
        setattr(db_comment, key, value)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: str) -> models.Comment:
    """コメントを削除する関数

    Args:
        db (Session): DBセッション
        comment_id (str): 削除するコメントのID

    Returns:
        models.Comment: 削除されたコメント
    """
    db_comment = (
        db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    )
    db.delete(db_comment)
    db.commit()
    return db_comment
