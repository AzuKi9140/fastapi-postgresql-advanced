from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    """投稿のベースモデル"""

    title: str
    content: str


class PostCreate(PostBase):
    """投稿の作成モデル"""

    user_id: str


class PostResponse(PostBase):
    """投稿のレスポンスモデル"""

    id: str
    user_id: str

    model_config = {"from_attributes": True}


class PostUpdate(PostBase):
    """投稿の更新モデル"""

    title: Optional[str] = None
    content: Optional[str] = None
