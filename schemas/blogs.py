from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema
from pydantic import Field
from fastapi import UploadFile


class CreateBlogMediaGroup(CreateBaseModel):
    blog_id: int
    filename: str

class BlogMediaGroupSchema(IdResponseSchema, CreateBlogMediaGroup):
    photo_url: str
    filename: str = Field(exclude=True)

class CreateBlogSchema(CreateBaseModel):
    title: str
    meta_description: str | None
    description: str
    media_group: list[UploadFile] = Field(exclude=True)

class UpdateBlogSchema(UpdateBaseModel, CreateBlogSchema):
    media_group: list[UploadFile] = Field(None, exclude=True)

class BlogSchema(IdResponseSchema, UpdateBlogSchema):

    photos: list[BlogMediaGroupSchema]