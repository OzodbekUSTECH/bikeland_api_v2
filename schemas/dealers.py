from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema
from pydantic import Field
from fastapi import UploadFile

class CreateDealerSchema(CreateBaseModel):
    full_name: str
    filename: UploadFile | None
    phone_number: str

class UpdateDealerSchema(UpdateBaseModel, CreateDealerSchema):
    pass

class DealerSchema(IdResponseSchema, UpdateDealerSchema):
    photo_url: str | None


    ################################
    filename: str | None = Field(exclude=True)