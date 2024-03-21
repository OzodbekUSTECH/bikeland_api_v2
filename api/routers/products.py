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
from fastapi_cache.decorator import cache
from fastapi_filter import FilterDepends, with_prefix
from utils.filters.filter_products import ProductFilters

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

# @router.post('')
# async def parse_1C_products() -> None:
#     await products_service.create_products()

from database import uow_dep
@router.post('/media')
async def create_media_group_for_product(
    uow: uow_dep,
    product_id: int,
    photos: list[UploadFile]
):
    return await products_service.create_media_group(uow, product_id, photos)

@router.get('', response_model=list[ProductSchema])
@cache(expire=600)
async def get_products(
    uow: uow_dep,
    filter_params: Annotated[FilterProductsParams, Depends()],
    prod_filter: ProductFilters = FilterDepends(ProductFilters)
):
    return await products_service.get_products(uow=uow, filter_params=filter_params, prod_filter=prod_filter)


# @router.get('/test-filter', response_model=list[ProductSchema])
# async def get_products(
#     uow: uow_dep,
#     # filter_params: Annotated[FilterProductsParams, Depends()],
#     # pagination: Annotated[pagination_params, Depends()],
#     prod_filter: ProductFilters = FilterDepends(ProductFilters)
# ):
#     return await products_service.get_filtered_products(uow, prod_filter)


@router.get('/duplicates')
async def get_duplicates(
    uow: uow_dep,
):
    return await products_service.get_only_duplicates(uow)

@router.get('/1c-db')
async def get_by_key_in_1c_db(key: str):
    return await products_service.get_product_1c_by_key(key)

@router.delete('/delete/{id}')
async def delete_product(
        uow: uow_dep, id: int
):
    return await products_service.delete_product(uow, id)

@router.get('/{id}', response_model=ProductSchema)
async def get_product_by_id(uow: uow_dep, id: int):
    return await products_service.get_product_by_id(uow, id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_product(
    uow: uow_dep,
    id: int,
    product_data: UpdateProductSchema,
    is_to_publish: bool = True,
):
    return await products_service.update_product(uow, is_to_publish, id, product_data)

@router.put('/{id}/archive', response_model=IdResponseSchema)
async def send_product_to_archive(uow: uow_dep, id: int):
    """
    Это роутер для самой карточки, кнопка В АРХИВ рядом с кнопкой 'РЕДАКТИРОВАТЬ!'
    """
    return await products_service.send_product_to_archive(uow, id)

@router.delete('/media/{id}', response_model=IdResponseSchema)
async def delete_photo(uow: uow_dep,id: int):
    return await products_service.delete_media(uow, id)
    