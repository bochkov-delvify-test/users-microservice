from typing import Never, Optional, Type

from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.orm import Session

from delvify.core import di
from delvify.crud import CRUDBase
from delvify.models import User
from delvify.schemas import UserCreate


class CRUDUser(CRUDBase[User, UserCreate, Never]):
    def __init__(self, db: Session, model: Type[User]):
        super().__init__(db, model)
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create(self, *, form: UserCreate) -> User:
        processed_form = UserCreate(
            email=form.email, password=self._hash_password(form.password)
        )
        return super().create(form=processed_form)

    def authenticate(self, *, email: EmailStr, password: str) -> Optional[User]:
        maybe_existing_user = self.get_by_email(email=email)
        if not maybe_existing_user:
            return None
        if not self._verify_password(password, maybe_existing_user.password):  # type: ignore
            return None
        return maybe_existing_user

    def get_by_email(self, *, email: EmailStr) -> Optional[User]:
        return self._db.query(User).filter(User.email == email).first()

    def _hash_password(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)


user = CRUDUser(db=di.get_db(), model=User)
