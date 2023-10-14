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

from database import uow_dep

@router.post('', response_model=IdResponseSchema)
async def create_blog(
    uow: uow_dep,
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
    return await blogs_service.create_blog(uow, blog_data)

@router.get('', response_model=Page[BlogSchema])
async def get_blogs(uow: uow_dep,):
    return await blogs_service.get_blogs(uow)

@router.get('/{id}', response_model=BlogSchema)
async def get_blog_by_id(
    id: int,
    uow: uow_dep,
):
    return await blogs_service.get_blog_by_id(uow, id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_blog(
    id: int,
    uow: uow_dep,
    title: str = Form(),
    meta_description: str | None = Form(None),
    description: str = Form(),
):
    blog_data = UpdateBlogSchema(
        title=title,
        meta_description=meta_description,
        description=description,
    )
    return await blogs_service.update_blog(uow, id, blog_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_blog(
    id: int,
    uow: uow_dep,
):
    return await blogs_service.delete_blog(uow, id)

################################################################
@router.post('/media/{blog_id}')
async def add_media_group_to_blog(
    blog_id: int,
    media_group: list[UploadFile],
    uow: uow_dep,
):
    return await blogs_service.add_media_group(uow, blog_id, media_group)

@router.delete('/media/{id}', response_model=IdResponseSchema)
async def delete_photo(
    id: int,
    uow: uow_dep,
):
    return await blogs_service.delete_photo(uow, id)