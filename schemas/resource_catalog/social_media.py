from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema
from fastapi import UploadFile
from pydantic import Field
class CreateSocialNetworkSchema(CreateBaseModel):
    type: str
    link: str
    filename: UploadFile | None

class UpdateSocialNetworkSchema(UpdateBaseModel, CreateSocialNetworkSchema):
    pass

class SocialNetworkSchema(IdResponseSchema, UpdateSocialNetworkSchema):
    photo_url: str

    filename: str = Field(exclude=True)
