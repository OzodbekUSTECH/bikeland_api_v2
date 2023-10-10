from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema


class CreateBrandSchema(CreateBaseModel):
    name: str

class UpdateBrandSchema(UpdateBaseModel, CreateBrandSchema):
    pass

class BrandSchema(IdResponseSchema, UpdateBrandSchema):
    pass