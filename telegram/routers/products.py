from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from telegram.services import products_service
from telegram.call_backs import SorterCallBackData, ChangeBrandCallBackData, PaginationProductsCallBackData

router = Router()

@router.message()
async def get_products_or_sub_categories(message: Message) -> None:
    await products_service.get_products(message)


@router.callback_query(PaginationProductsCallBackData.filter())
async def paginate_products(query: CallbackQuery, callback_data: PaginationProductsCallBackData):
    
    if callback_data.name == "next_product":
        callback_data.current_page += 1
    elif callback_data.name == "prev_product":
        callback_data.current_page -= 1

    await products_service.paginate_products(
        query=query,
        category_id=callback_data.category_id,
        sub_category_id=callback_data.sub_category_id,
        current_page=callback_data.current_page,
        sort_by=callback_data.sort_by,
        brand_name=callback_data.brand_name
    )

@router.callback_query(ChangeBrandCallBackData.filter())
async def change_brand(query: CallbackQuery, callback_data: ChangeBrandCallBackData) -> None:
    await products_service.change_brand(
        query=query,
        callback_data=callback_data,
    )


@router.callback_query(SorterCallBackData.filter())
async def sort_products(query: CallbackQuery, callback_data: SorterCallBackData) -> None:
    await products_service.sort_products(query=query, callback_data=callback_data)