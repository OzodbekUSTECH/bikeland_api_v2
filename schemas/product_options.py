from schemas import CreateBaseModel,  UpdateBaseModel, IdResponseSchema


class CreateMultipleProductOptions(CreateBaseModel):
    name: str
    price: float

class CreateProductOptionSchema(CreateBaseModel):
    product_id: int
    name: str
    price: float

class UpdateProductOptionSchema(UpdateBaseModel, CreateProductOptionSchema):
    pass

class ProductOptionSchema(IdResponseSchema, UpdateProductOptionSchema):
    pass
