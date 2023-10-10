from fastapi import APIRouter
from services import sub_categories_service
from repositories import Page
from schemas.sub_categories import (
    CreateSubCategorySchema,
    UpdateSubCategorySchema,
)
from schemas import IdResponseSchema

router = APIRouter(
    prefix="/sub-categories",
    tags=["Sub Categories"],
)

@router.post('', response_model=IdResponseSchema)
async def create_sub_category(
    sub_category_data: CreateSubCategorySchema
):
    return await sub_categories_service.create_sub_category(sub_category_data)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_sub_category(
    id: int,
    sub_category_data: UpdateSubCategorySchema
):
    return await sub_categories_service.update_sub_category(id, sub_category_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_sub_category(
    id: int
):
    return await sub_categories_service.delete_sub_category(id)