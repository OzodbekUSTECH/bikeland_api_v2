from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema
from schemas.sub_categories import SubCategorySchema

class CreateCategorySchema(CreateBaseModel):
    name: str

class UpdateCategorySchema(UpdateBaseModel, CreateCategorySchema):
    pass

class CategorySchema(IdResponseSchema, UpdateCategorySchema):
    sub_categories: list[SubCategorySchema]