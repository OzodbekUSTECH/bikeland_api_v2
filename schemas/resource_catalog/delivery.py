from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema
from pydantic import Field
class CreateDeliverySchema(CreateBaseModel):
    title: str
    description: str

class UpdateDeliverySchema(UpdateBaseModel, CreateDeliverySchema):
    pass

class DeliverySchema(IdResponseSchema, UpdateDeliverySchema):
    pass

################################################################

class CreateDeliveryMediaSchema(CreateBaseModel):
    filename: str

class DeliveryMediaSchema(IdResponseSchema, CreateDeliveryMediaSchema):
    photo_url: str

    filename: str = Field(exclude=True)

