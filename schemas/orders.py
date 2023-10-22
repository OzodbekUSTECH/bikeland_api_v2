from schemas import CreateBaseModel,  IdResponseSchema
from pydantic import Field
from schemas.product_options import ProductOptionSchema



class CreateOrderBasketSchema(CreateBaseModel):
    product_id: int
    quantity: int
    option_ids: list[int] | None

################################
class CreateCustomOrderBasketSchema(CreateOrderBasketSchema):
    order_id: int
    tgclient_id: int
################################

class OrderBasketSchema(IdResponseSchema, CreateOrderBasketSchema):
    title_of_product: str
    type_of_product: str | None
    price: float
    price_with_options: float | None
    options: list[ProductOptionSchema]

################################
class CreateOrderSchema(CreateBaseModel):
    name: str
    phone_number: str
    region: str
    known_from: str | None
    basket: list[CreateOrderBasketSchema] = Field(exclude=True)

class OrderSchema(IdResponseSchema, CreateOrderSchema):
    total_price: float
    basket: list[OrderBasketSchema]