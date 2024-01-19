from fastapi import APIRouter, BackgroundTasks
from services import product_video_links_service
from schemas.product_video_links import (
    CreateProductVideoLinkShema,
    UpdateProductVideoLinkSchema,
    ProductVideoLinkSchema, 
)
from schemas import IdResponseSchema
from repositories import Page
from database import uow_dep

router = APIRouter(
    prefix="/video-links",
    tags=["Product Video Links", ],
)

@router.post('', response_model=IdResponseSchema)
async def create_product_video_link(
    uow: uow_dep,
    data: CreateProductVideoLinkShema
):
    return await product_video_links_service.create_product_video_link(uow, data)

# @router.get('/moving')
# async def move_solo_video_link_to_multiple_links(uow: uow_dep):
#     return await product_video_links_service.move_solo_video_link_to_multiple_links(uow)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_product_video_link(
    uow: uow_dep,
    id: int,
    data: UpdateProductVideoLinkSchema
):
    return await product_video_links_service.update_product_video_link(uow, id, data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_product_video_link(
    uow: uow_dep,
    id: int
):
    return await product_video_links_service.delete_product_video_link(uow, id)