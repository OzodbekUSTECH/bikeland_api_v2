from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema
from pydantic import Field
from fastapi import UploadFile
from schemas.waiting_lists import WaitingListSchema

class CreateDealerSchema(CreateBaseModel):
    full_name: str
    filename: UploadFile | None
    phone_number: str

class UpdateDealerSchema(UpdateBaseModel, CreateDealerSchema):
    pass

class DealerSchema(IdResponseSchema, UpdateDealerSchema):
    photo_url: str | None
    waiting_list: list[WaitingListSchema]

    ################################
    filename: str | None = Field(exclude=True)