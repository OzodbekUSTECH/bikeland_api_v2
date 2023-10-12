from schemas import CreateBaseModel,  IdResponseSchema


class CreateOrderSchema(CreateBaseModel):
    name: str
    phone_number: str
    region: str
    known_from: str
    quantity: int
    product_id: int

class OrderSchema(IdResponseSchema, CreateOrderSchema):
    price: int
    product_title: str
    brand_name: str | None
    source: str