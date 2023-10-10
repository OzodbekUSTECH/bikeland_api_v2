from pydantic import BaseModel, Field
from datetime import datetime

def get_current_time():
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")

datetime_field = Field(example=datetime.now().strftime("%d.%m.%Y %H:%M:%S"), default_factory=get_current_time)

class IdResponseSchema(BaseModel):
    id: int
    created_at: str


class CreateBaseModel(BaseModel):
    created_at: str = datetime_field


class UpdateBaseModel(BaseModel):
    created_at: str = Field(None , exclude=True)
    updated_at: str | None = datetime_field
