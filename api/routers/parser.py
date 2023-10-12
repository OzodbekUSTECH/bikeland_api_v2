from fastapi import APIRouter, BackgroundTasks
from services import parser_service
from repositories import Page

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
async def parse_own_products(
    bg: BackgroundTasks
):
    bg.add_task(parser_service.parse_own_products)

@router.get('/correct-photos')
async def corret_the_order_of_photos(
    bg: BackgroundTasks
):
    bg.add_task(parser_service.change_the_order_of_photos)