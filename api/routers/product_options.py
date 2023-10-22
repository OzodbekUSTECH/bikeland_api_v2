from fastapi import APIRouter, BackgroundTasks
from services import product_options_service
from schemas.product_options import (
    CreateMultipleProductOptions,
    CreateProductOptionSchema,
    UpdateProductOptionSchema,
    ProductOptionSchema,
)
from schemas import IdResponseSchema
from repositories import Page
from database import uow_dep

router = APIRouter(
    prefix="/options",
    tags=["Product Options", ],
)

@router.post('/multiple')
async def create_multiple_product_options(
    uow: uow_dep,
    product_id: int,
    options: list[CreateMultipleProductOptions]
):
    return await product_options_service.create_multiple_product_options(uow, product_id, options)

@router.post('', response_model=IdResponseSchema)
async def create_product_option(
    uow: uow_dep,
    option_data: CreateProductOptionSchema
):
    return await product_options_service.create_product_option(uow, option_data)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_product_option(
    uow: uow_dep,
    id: int,
    option_data: UpdateProductOptionSchema
):
    return await product_options_service.update_product_option(uow, id, option_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_product_option(
    uow: uow_dep,
    id: int
):
    return await product_options_service.delete_product_option(uow, id)
