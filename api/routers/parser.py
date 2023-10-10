from fastapi import APIRouter, UploadFile
from services import parser_service
from repositories import Page
from schemas.products import (
    UpdateProductSchema,
    ProductSchema,
)
from schemas import IdResponseSchema
from repositories import pagination_params
from utils.filters.filter_products import FilterProductsParams

router = APIRouter(
    prefix="/parser",
    tags=["Parser for own products"],
)
@router.get('/categories')
async def parse_own_categories():
    return await parser_service.parse_own_categories()
@router.get('/sub-categories')
async def parse_own_sub_categories():
    return await parser_service.parse_own_sub_categories()
@router.get('/brands')
async def parse_own_brands():
    """
    should start from 6...
    """
    return await parser_service.parse_own_brands()

@router.get('/products')
async def parse_own_products():
    return await parser_service.parse_own_products()