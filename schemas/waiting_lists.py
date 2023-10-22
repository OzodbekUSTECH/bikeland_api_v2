from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema
from pydantic import Field
class CreateWaitingListSchema(CreateBaseModel):
    dealer_id: int
    product_id: int

class WaitingListSchema(IdResponseSchema, CreateWaitingListSchema):
    title_of_product: str
    key_of_product: str
    quantity: int
    min_quantity: int
    required_quantity: int

    dealer_id: int = Field(exclude=True)