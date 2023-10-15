from aiogram import Router, F
from aiogram.types import Message
from telegram.services import categories_service
from telegram.btn_names import WelcomeBtnNames
from database import UnitOfWork

router = Router()

@router.message(F.text == WelcomeBtnNames.BIKE.value)
async def get_list_of_categories(message: Message, uow = UnitOfWork()) -> None:
    async with uow:
        await categories_service.get_list_of_motorbike_categories(message=message, uow=uow)



@router.message(F.text == WelcomeBtnNames.EQUIPS.value)
async def get_list_of_categories(message: Message, uow = UnitOfWork()) -> None:
    async with uow:
        await categories_service.get_list_of_equips(message, uow)







