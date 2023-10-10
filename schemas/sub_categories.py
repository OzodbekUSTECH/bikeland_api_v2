from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema


class CreateSubCategorySchema(CreateBaseModel):
    category_id: int
    name: str

class UpdateSubCategorySchema(UpdateBaseModel, CreateSubCategorySchema):
    pass

class SubCategorySchema(IdResponseSchema, UpdateSubCategorySchema):
    pass