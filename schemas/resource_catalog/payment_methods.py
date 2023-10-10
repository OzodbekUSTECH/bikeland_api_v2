from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema
from fastapi import UploadFile
from pydantic import Field

class CreatePaymentMethodSchema(CreateBaseModel):
    type: str
    filename: UploadFile | None

class UpdatePaymentMethodSchema(UpdateBaseModel, CreatePaymentMethodSchema):
    pass

class PaymentMethodSchema(IdResponseSchema, UpdatePaymentMethodSchema):
    photo_url: str

    filename: str = Field(exclude=True)
