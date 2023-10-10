from fastapi import APIRouter, Form, UploadFile, File
from services import blogs_service
from repositories import Page
from schemas.blogs import (
    CreateBlogSchema,
    UpdateBlogSchema,
    BlogSchema,
)
from schemas import IdResponseSchema

router = APIRouter(
    prefix="/blogs",
    tags=["Blogs and Media Group(photos)"],
)

@router.post('', response_model=IdResponseSchema)
async def create_blog(
    title: str = Form(),
    meta_description: str | None = Form(None),
    description: str = Form(),
    media_group: list[UploadFile] = File()
):
    blog_data = CreateBlogSchema(
        title=title,
        meta_description=meta_description,
        description=description,
        media_group=media_group
    )
    return await blogs_service.create_blog(blog_data)

@router.get('', response_model=Page[BlogSchema])
async def get_blogs():
    return await blogs_service.get_blogs()

@router.get('/{id}', response_model=BlogSchema)
async def get_blog_by_id(
    id: int
):
    return await blogs_service.get_blog_by_id(id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_blog(
    id: int,
    title: str = Form(),
    meta_description: str | None = Form(None),
    description: str = Form(),
):
    blog_data = UpdateBlogSchema(
        title=title,
        meta_description=meta_description,
        description=description,
    )
    return await blogs_service.update_blog(id, blog_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_blog(
    id: int
):
    return await blogs_service.delete_blog(id)

################################################################
@router.post('/media/{blog_id}')
async def add_media_group_to_blog(
    blog_id: int,
    media_group: list[UploadFile]
):
    return await blogs_service.add_media_group(blog_id, media_group)

@router.delete('/media/{id}', response_model=IdResponseSchema)
async def delete_photo(
    id: int
):
    return await blogs_service.delete_photo(id)