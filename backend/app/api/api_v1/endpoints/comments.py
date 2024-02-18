from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import (
    crud,  # ユーザー作成のロジックを含む関数をインポート
    schemas,  # 作成したPydanticモデルをインポート
)
from app.api import deps  # 作成した依存性をインポート

router = APIRouter()


@router.patch("/{comment_id}", response_model=schemas.CommentResponse)
async def update_comment_endpoint(
    comment_id: str, comment: schemas.CommentUpdate, db: Session = Depends(deps.get_db)
) -> schemas.CommentResponse:
    """コメントを更新するエンドポイント

    Args:
        comment_id (str): 更新するコメントのID
        comment (schemas.CommentUpdate): 更新するコメントの情報
        db (Session, optional): DBセッション. Defaults to Depends(get_db).

    Raises:
        HTTPException: コメントが見つからない場合に発生

    Returns:
        CommentResponse: 更新されたコメントの情報
    """

    # コメントが存在するか確認
    db_comment = crud.get_comment_by_id(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    updated_comment = crud.update_comment(db, comment_id, comment)

    return updated_comment


@router.delete("/{comment_id}", response_model=schemas.CommentResponse)
async def delete_comment_endpoint(
    comment_id: str, db: Session = Depends(deps.get_db)
) -> schemas.CommentResponse:
    """コメントを削除するエンドポイント

    Args:
        comment_id (str): 削除するコメントのID
        db (Session, optional): DBセッション. Defaults to Depends(get_db).

    Raises:
        HTTPException: コメントが見つからない場合に発生

    Returns:
        CommentResponse: 削除されたコメントの情報
    """

    # コメントが存在するか確認
    db_comment = crud.get_comment_by_id(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    deleted_comment = crud.delete_comment(db, comment_id)

    return deleted_comment
