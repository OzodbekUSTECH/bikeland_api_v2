from fastapi import APIRouter, BackgroundTasks
from services import parser_service
from repositories import Page

router = APIRouter(
    prefix="/parser",
    tags=["Parser for own products"],
)

from database import uow_dep

@router.get('/categories')
async def parse_own_categories(uow: uow_dep):
    return await parser_service.parse_own_categories(uow)
@router.get('/sub-categories')
async def parse_own_sub_categories(uow: uow_dep):
    return await parser_service.parse_own_sub_categories(uow)

@router.get('/blogs')
async def parse_own_blogs(
    bg: BackgroundTasks,
    uow: uow_dep,
):
    bg.add_task(parser_service.parse_own_blogs, uow)

@router.get('/brands')
async def parse_own_brands(uow: uow_dep):
    """
    should start from 6...
    """
    return await parser_service.parse_own_brands(uow)

@router.get('/products')
async def parse_own_products(
    bg: BackgroundTasks,
    uow: uow_dep
):
    bg.add_task(parser_service.parse_own_products, uow)

@router.get('/correct-photos')
async def corret_the_order_of_photos(
    bg: BackgroundTasks,
    uow: uow_dep
):
    bg.add_task(parser_service.change_the_order_of_photos, uow)