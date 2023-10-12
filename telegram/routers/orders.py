from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from telegram.services import orders_service
from telegram.call_backs import OrderCallBackData
from aiogram.fsm.context import FSMContext
from telegram.states import OrderStates

router = Router()


@router.callback_query(OrderCallBackData.filter())
async def ask_for_region(query: CallbackQuery, callback_data: OrderCallBackData, state: FSMContext) -> None:
    await orders_service.get_product_id(
        query = query,
        state=state,
        product_id=callback_data.product_id
    )


@router.message(OrderStates.region)
async def get_region(message: Message, state: FSMContext) -> None:
    if message.text == "Отменить":
        await orders_service.cancel_ordering(message, state)
    else:
        await orders_service.get_region(message, state)


@router.message(OrderStates.name)
async def get_name(message: Message, state: FSMContext) -> None:
    if message.text == "Отменить":
        await orders_service.cancel_ordering(message, state)
    else:
        await orders_service.get_name(message, state)


@router.message(OrderStates.phone_number)
async def get_phone_number(message: Message, state: FSMContext) -> None:
    if message.text == "Отменить":
        await orders_service.cancel_ordering(message, state)
    else:
        await orders_service.get_phone_number(message, state)

@router.message(OrderStates.quantity)
async def get_quantity_and_show_order_data(message: Message, state: FSMContext) -> None:
    if message.text == "Отменить":
        await orders_service.cancel_ordering(message, state)
    else:
        await orders_service.get_quantity_and_show_order_data(message, state)

