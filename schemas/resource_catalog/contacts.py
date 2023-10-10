from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema
from fastapi import UploadFile
from pydantic import Field

class CreateContactSchema(CreateBaseModel):
    type: str
    data: str
    filename: UploadFile | None

class UpdateContactSchema(UpdateBaseModel, CreateContactSchema):
    pass

class ContactSchema(IdResponseSchema, UpdateContactSchema):
    photo_url: str

    filename: str = Field(exclude=True)