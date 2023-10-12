from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from telegram.btn_names import WelcomeBtnNames
from telegram.services import basket_service
from telegram.call_backs import PaginationBasketCallbackData
router = Router()


@router.message(F.text == WelcomeBtnNames.BASKET.value)
async def get_basket_of_client(message: Message) -> None:
    await basket_service.show_basket(message)


@router.callback_query(PaginationBasketCallbackData.filter())
async def paginate_basket_products(query: CallbackQuery, callback_data: PaginationBasketCallbackData) -> None:
    if callback_data.name == "next_product":
        callback_data.current_page += 1
    elif callback_data.name == "prev_product":
        callback_data.current_page -= 1

    await basket_service.paginate_basket(
        query=query,
        current_page=callback_data.current_page,
    )
