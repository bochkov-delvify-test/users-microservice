from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(UserCreate):
    pass


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
