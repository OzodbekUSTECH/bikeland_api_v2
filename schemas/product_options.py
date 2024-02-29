from schemas import CreateBaseModel,  UpdateBaseModel, IdResponseSchema
from pydantic import Field

class CreateMultipleProductOptions(CreateBaseModel):
    name: str
    price: int

class CreateProductOptionSchema(CreateBaseModel):
    product_id: int
    name: str
    price: int

class UpdateProductOptionSchema(UpdateBaseModel, CreateProductOptionSchema):
    pass

class ProductOptionSchema(IdResponseSchema, UpdateProductOptionSchema):
    pass  
