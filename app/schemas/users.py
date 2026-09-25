from pydantic import BaseModel, ConfigDict, EmailStr

class UserCreateSchema(BaseModel):

    username: str
    email: str
    password: str
    is_superuser: bool 

class UserReadSchema(BaseModel):

    id: int
    username: str
    email: str
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)

class UserAuthSchema(BaseModel):

    email: EmailStr
    password: str