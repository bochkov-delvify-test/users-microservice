from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException

from delvify import crud, models, schemas
from delvify.core import di
from delvify.core.security import create_access_token
from delvify.schemas import Jwt, JwtPayload

endpoint = APIRouter()


@endpoint.post("", response_model=schemas.User)
def create_user(
    *,
    form: schemas.UserCreate,
) -> Any:
    maybe_user = crud.user.get_by_email(email=form.email)
    if maybe_user:
        raise HTTPException(
            status_code=400, detail="The user with this email, already exists."
        )
    return crud.user.create(form=form)


@endpoint.post("/login", response_model=Jwt)
def login(form: schemas.UserLogin) -> Any:
    maybe_user: Optional[models.User] = crud.user.authenticate(
        email=form.email, password=form.password
    )
    if maybe_user is None:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return Jwt(
        access_token=create_access_token(
            JwtPayload(user_id=maybe_user.id).model_dump()  # type: ignore
        ),
        token_type="bearer",
    )


@endpoint.get("/me", response_model=schemas.User)
def get_user_me(user_id: int = Depends(di.get_current_user_id)) -> Any:
    user = crud.user.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
