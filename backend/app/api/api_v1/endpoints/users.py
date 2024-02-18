from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import (
    crud,  # ユーザー作成のロジックを含む関数をインポート
    schemas,  # 作成したPydanticモデルをインポート
)
from app.api import deps  # 作成した依存性をインポート

router = APIRouter()


@router.post("/", response_model=schemas.UserResponse, status_code=201)
async def create_user_endpoint(
    user: schemas.UserCreate, db: Session = Depends(deps.get_db)
) -> schemas.UserResponse:
    """ユーザーを作成するエンドポイント

    Args:
        user (schemas.UserCreate): 作成するユーザーの情報
        db (Session, optional): DBセッション. Defaults to Depends(get_db).

    Raises:
        HTTPException: ユーザーが作成できなかった場合に発生

    Returns:
        UserResponse: 作成されたユーザーの情報
    """
    created_user = crud.create_user(db, user)
    if created_user:
        return created_user
    else:
        raise HTTPException(status_code=400, detail="User could not be created")


@router.get("/", response_model=List[schemas.UserResponse])
async def read_users(db: Session = Depends(deps.get_db)) -> List[schemas.UserResponse]:
    """ユーザーの一覧を取得するエンドポイント

    Args:
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Returns:
        List[schemas.UserResponse]: 取得されたユーザーの一覧
    """
    users = crud.get_users(db)
    return users


@router.get("/{user_id}", response_model=schemas.UserResponse)
async def read_user(
    user_id: str, db: Session = Depends(deps.get_db)
) -> schemas.UserResponse:
    """ユーザーの詳細を取得するエンドポイント

    Args:
        user_id (str): 取得するユーザーのID
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Exceptions:
        HTTPException: ユーザーが見つからない場合に発生
    Returns:
        schemas.UserResponse: 取得されたユーザーの情報
    """
    user = crud.get_user_by_uid(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=schemas.UserResponse)
async def update_user(
    user_id: str, user: schemas.UserCreate, db: Session = Depends(deps.get_db)
) -> schemas.UserResponse:
    """ユーザーを更新するエンドポイント

    Args:
        user_id (str): 更新するユーザーのID
        user (schemas.UserCreate): 更新するユーザーの情報
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Exceptions:
        HTTPException: ユーザーが見つからない場合に発生

    Returns:
        schemas.UserResponse: 更新されたユーザーの情報
    """
    # ユーザーが見つからない場合は404エラーを返す
    existing_user = crud.get_user_by_uid(db, user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = crud.update_user(db, user_id, user)

    return updated_user


@router.delete("/{user_id}", response_model=schemas.UserResponse)
async def delete_user(
    user_id: str, db: Session = Depends(deps.get_db)
) -> schemas.UserResponse:
    """ユーザーを削除するエンドポイント

    Args:
        user_id (str): 削除するユーザーのID
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Exceptions:
        HTTPException: ユーザーが見つからない場合に発生

    Returns:
        schemas.UserResponse: 削除されたユーザーの情報
    """
    # ユーザーが見つからない場合は404エラーを返す
    existing_user = crud.get_user_by_uid(db, user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    deleted_user = crud.delete_user(db, user_id)

    return deleted_user


@router.get("/{user_id}/posts", response_model=List[schemas.PostResponse])
async def read_user_posts(
    user_id: str, db: Session = Depends(deps.get_db)
) -> List[schemas.PostResponse]:
    """ユーザーの投稿の一覧を取得するエンドポイント

    Args:
        user_id (str): 取得するユーザーのID
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Exceptions:
        HTTPException: ユーザーが見つからない場合に発生

    Returns:
        List[schemas.PostResponse]: 取得された投稿の一覧
    """
    # ユーザーが見つからない場合は404エラーを返す
    existing_user = crud.get_user_by_uid(db, user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    posts = crud.get_posts_by_user_id(db, user_id)
    return posts
