from datetime import datetime, timedelta
from typing import Any

from jose import jwt

from delvify.core import app_settings


def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(
        minutes=app_settings.ACCESS_TOKEN_EXPIRATION_MINUTES
    )
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(
        to_encode,
        key=app_settings.SECRET_KEY.get_secret_value(),
        algorithm=app_settings.TOKEN_ALGORITHM,
    )
    return encoded_jwt
