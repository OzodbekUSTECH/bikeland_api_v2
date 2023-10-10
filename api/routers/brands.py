from fastapi import APIRouter
from services import brands_service
from repositories import Page
from schemas.brands import (
    CreateBrandSchema,
    UpdateBrandSchema,
    BrandSchema,
)
from schemas import IdResponseSchema

router = APIRouter(
    prefix="/brands",
    tags=["Brands"],
)

@router.post('', response_model=IdResponseSchema)
async def create_brand(
    brand_data: CreateBrandSchema
):
    return await brands_service.create_brand(brand_data)

@router.get('', response_model=Page[BrandSchema])
async def get_brands():
    return await brands_service.get_brands()

@router.get('/{id}', response_model=BrandSchema)
async def get_brand_by_id(
    id: int
):
    return await brands_service.get_brand_by_id(id)

@router.put('/{id}', response_model=BrandSchema)
async def update_brand(
    id: int,
    brand_data: UpdateBrandSchema
):
    return await brands_service.update_brand(id, brand_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_brand(
    id: int
):
    return await brands_service.delete_brand(id)
