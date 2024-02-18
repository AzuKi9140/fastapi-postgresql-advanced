from typing import Optional

from pydantic import BaseModel


class CommentBase(BaseModel):
    """コメントのベースモデル"""

    content: str


class CommentCreate(CommentBase):
    """コメントの作成モデル"""

    user_id: str


class CommentResponse(CommentBase):
    """コメントのレスポンスモデル"""

    id: str
    user_id: str
    post_id: str

    model_config = {"from_attributes": True}


class CommentUpdate(CommentBase):
    """コメントの更新モデル"""

    content: Optional[str] = None

class CommentWithUserResponse(CommentResponse):
    """コメントのレスポンスモデル（ユーザー情報付き）"""

    user_name: str
    model_config = {"from_attributes": True}
