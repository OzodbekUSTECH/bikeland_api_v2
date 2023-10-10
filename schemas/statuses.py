from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema

class CreateStatusSchema(CreateBaseModel):
    name: str

class UpdateStatusSchema(UpdateBaseModel, CreateStatusSchema):
    pass

class StatusSchema(IdResponseSchema, UpdateStatusSchema):
    pass