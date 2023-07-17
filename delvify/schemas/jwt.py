from typing import Literal, Optional

from pydantic import BaseModel


class Jwt(BaseModel):
    access_token: str
    token_type: Literal["bearer"]


class JwtPayload(BaseModel):
    user_id: Optional[int]
