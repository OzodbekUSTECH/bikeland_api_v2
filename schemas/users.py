from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema
from pydantic import EmailStr, Field, BaseModel
from fastapi import File, UploadFile

class BaseUserSchema(CreateBaseModel):
    full_name: str
    filename: UploadFile | None
    email: EmailStr
    phone_number: str


class CreateUserSchema(BaseUserSchema):
    password: str = Field(min_length=8, max_length=64)


class UpdateUserSchema(UpdateBaseModel, BaseUserSchema):
    pass

class UserSchema(IdResponseSchema, UpdateUserSchema):
    photo_url: str | None


    ################################
    filename: str | None = Field(exclude=True)





#################################
class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class ResetPasswordSchema(BaseModel):
    password: str = Field(min_length=8, max_length=64)

   
