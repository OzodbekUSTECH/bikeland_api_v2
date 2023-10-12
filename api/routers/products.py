from fastapi import APIRouter, UploadFile, Depends
from services import products_service
from repositories import Page
from schemas.products import (
    UpdateProductSchema,
    ProductSchema,
)
from schemas import IdResponseSchema
from repositories import pagination_params
from utils.filters.filter_products import FilterProductsParams
from typing import Annotated

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

# @router.post('')
# async def parse_1C_products() -> None:
#     await products_service.create_products()


@router.post('/media')
async def create_media_group_for_product(
    product_id: int,
    photos: list[UploadFile]
):
    return await products_service.create_media_group(product_id, photos)

@router.get('', response_model=Page[ProductSchema] | list[ProductSchema])
async def get_products(
    filter_params: Annotated[FilterProductsParams, Depends()],
    pagination: Annotated[pagination_params, Depends()]
):
    return await products_service.get_products(filter_params, pagination)

@router.get('/{id}', response_model=ProductSchema)
async def get_product_by_id(id: int):
    return await products_service.get_product_by_id(id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_product(
    id: int,
    product_data: UpdateProductSchema,
    is_to_publish: bool = True,
):
    return await products_service.update_product(is_to_publish, id, product_data)

@router.put('/{id}/archive', response_model=IdResponseSchema)
async def send_product_to_archive(id: int):
    """
    Это роутер для самой карточки, кнопка В АРХИВ рядом с кнопкой 'РЕДАКТИРОВАТЬ!'
    """
    return await products_service.send_product_to_archive(id)

@router.delete('/media/{id}', response_model=IdResponseSchema)
async def delete_photo(id: int):
    return await products_service.delete_media(id)
    