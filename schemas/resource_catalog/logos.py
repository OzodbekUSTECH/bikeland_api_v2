from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema
from fastapi import UploadFile
from pydantic import Field

class CreateLogoSchema(CreateBaseModel):
    filename: UploadFile

class UpdateLogoSchema(UpdateBaseModel, CreateLogoSchema):
    pass

class LogoSchema(IdResponseSchema, UpdateLogoSchema):
    photo_url: str

    filename: str = Field(exclude=True)