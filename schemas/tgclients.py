from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema


class CreateTgClientSchema(CreateBaseModel):
    telegram_id: int | None = None
    full_name: str | None = None
    username: str | None = None
    phone_number: str

class UpdateTgClientSchema(UpdateBaseModel, CreateTgClientSchema):
    pass

class TgClientSchema(IdResponseSchema, UpdateTgClientSchema):
    pass