from schemas import CreateBaseModel,  UpdateBaseModel, IdResponseSchema
from pydantic import Field


class CreateProductVideoLinkShema(CreateBaseModel):
    product_id: int
    name: str
    link: str

class UpdateProductVideoLinkSchema(UpdateBaseModel, CreateProductVideoLinkShema):
    pass

class ProductVideoLinkSchema(IdResponseSchema, UpdateProductVideoLinkSchema):
    pass