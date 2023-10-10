from fastapi import APIRouter
from services import categories_service
from repositories import Page
from schemas.categories import (
    CreateCategorySchema,
    UpdateCategorySchema,
    CategorySchema,
)
from schemas import IdResponseSchema

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

@router.post('', response_model=IdResponseSchema)
async def create_category(
    category_data: CreateCategorySchema
):
    return await categories_service.create_category(category_data)

@router.get('', response_model=Page[CategorySchema])
async def get_categories():
    return await categories_service.get_categories()

@router.get('/{id}', response_model=CategorySchema)
async def get_category_by_id(
    id: int
):
    return await categories_service.get_category_by_id(id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_category(
    id: int,
    category_data: UpdateCategorySchema
):
    return await categories_service.update_category(id, category_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_category(
    id: int
):
    return await categories_service.delete_category(id)