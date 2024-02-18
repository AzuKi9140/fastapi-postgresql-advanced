from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import (
    crud,  # ユーザー作成のロジックを含む関数をインポート
    schemas,  # 作成したPydanticモデルをインポート
)
from app.api import deps  # 作成した依存性をインポート

router = APIRouter()


@router.post("/", response_model=schemas.PostResponse, status_code=201)
async def create_post_endpoint(
    post: schemas.PostCreate, db: Session = Depends(deps.get_db)
) -> schemas.PostResponse:
    """投稿を作成するエンドポイント

    Args:
        post (schemas.PostCreate): 作成する投稿の情報
        db (Session, optional): DBセッション. Defaults to Depends(get_db).

    Raises:
        HTTPException: ユーザーが存在しない場合に発生

    Returns:
        PostResponse: 作成された投稿の情報
    """

    # ユーザーが存在するか確認
    user = crud.get_user_by_uid(db, user_id=post.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    created_post = crud.create_post(db, post)
    if created_post:
        return created_post
    else:
        raise HTTPException(status_code=400, detail="Post could not be created")


@router.get("/", response_model=List[schemas.PostResponse])
async def read_posts(db: Session = Depends(deps.get_db)) -> List[schemas.PostResponse]:
    """投稿の一覧を取得するエンドポイント

    Args:
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Returns:
        List[schemas.PostResponse]: 取得された投稿の一覧
    """
    posts = crud.get_posts(db)
    return posts


@router.get("/{post_id}", response_model=schemas.PostResponse)
async def read_post(
    post_id: str, db: Session = Depends(deps.get_db)
) -> schemas.PostResponse:
    """投稿の詳細を取得するエンドポイント

    Args:
        post_id (str): 取得する投稿のID
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: 投稿が存在しない場合に発生

    Returns:
        schemas.PostResponse: 取得された投稿の情報
    """
    post = crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.patch("/{post_id}", response_model=schemas.PostResponse)
async def update_post(
    post_id: str, post: schemas.PostUpdate, db: Session = Depends(deps.get_db)
) -> schemas.PostResponse:
    """投稿を更新するエンドポイント

    Args:
        post_id (str): 更新する投稿のID
        post (schemas.PostUpdate): 更新する投稿の情報
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Returns:
        schemas.PostResponse: 更新された投稿の情報
    """
    # 投稿が存在するか確認
    existing_post = crud.get_post_by_id(db, post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    updated_post = crud.update_post(db, post_id, post)
    return updated_post


@router.delete("/{post_id}", response_model=schemas.PostResponse)
async def delete_post(
    post_id: str, db: Session = Depends(deps.get_db)
) -> schemas.PostResponse:
    """投稿を削除するエンドポイント

    Args:
        post_id (str): 削除する投稿のID
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Returns:
        schemas.PostResponse: 削除された投稿の情報
    """
    # 投稿が存在するか確認
    existing_post = crud.get_post_by_id(db, post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    deleted_post = crud.delete_post(db, post_id)
    return deleted_post


@router.post(
    "/{post_id}/comments/", response_model=schemas.CommentResponse, status_code=201
)
async def create_comment_for_post(
    post_id: str, comment: schemas.CommentCreate, db: Session = Depends(deps.get_db)
) -> schemas.CommentResponse:
    """投稿にコメントを作成するエンドポイント

    Args:
        post_id (str): コメントを作成する投稿のID
        comment (schemas.CommentCreate): 作成するコメントの情報
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: 投稿が存在しない場合に発生

    Returns:
        CommentResponse: 作成されたコメントの情報
    """
    # 投稿が存在するか確認
    existing_post = crud.get_post_by_id(db, post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    created_comment = crud.create_comment_for_post(db, comment, post_id)

    return created_comment


@router.get(
    "/{post_id}/comments/", response_model=List[schemas.CommentWithUserResponse]
)
async def read_comments_for_post(
    post_id: str, db: Session = Depends(deps.get_db)
) -> List[schemas.CommentWithUserResponse]:
    """投稿に紐づくコメントの一覧を取得するエンドポイント

    Args:
        post_id (str): 取得するコメントの投稿のID
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: 投稿が存在しない場合に発生

    Returns:
        List[schemas.CommentWithUserResponse]: 取得されたコメントの一覧
    """
    # 投稿が存在するか確認
    existing_post = crud.get_post_by_id(db, post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    comments = crud.get_comments_for_post(db, post_id)
    comments_with_user = [
        schemas.CommentWithUserResponse(
            id=comment.id,
            user_id=comment.user_id,
            post_id=comment.post_id,
            content=comment.content,
            user_name=comment.user.name,  # ここでリレーションシップ関係であるUserの情報を取得
        )
        for comment in comments
    ]
    return comments_with_user
