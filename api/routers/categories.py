from fastapi import APIRouter
from services import categories_service
from repositories import Page
from schemas.categories import (
    CreateCategorySchema,
    UpdateCategorySchema,
    CategorySchema,
)
from schemas import IdResponseSchema
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)
from database import uow_dep

@router.post('', response_model=IdResponseSchema)
async def create_category(
    category_data: CreateCategorySchema,
    uow: uow_dep,
):
    return await categories_service.create_category(uow, category_data)

@router.get('', response_model=Page[CategorySchema])
async def get_categories(uow: uow_dep,):
    return await categories_service.get_categories(uow)

@router.get('/{id}', response_model=CategorySchema)
async def get_category_by_id(
    id: int,
    uow: uow_dep,
):
    return await categories_service.get_category_by_id(uow, id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_category(
    id: int,
    uow: uow_dep,
    category_data: UpdateCategorySchema
):
    return await categories_service.update_category(uow, id, category_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_category(
    id: int,
    uow: uow_dep,
):
    return await categories_service.delete_category(uow, id)