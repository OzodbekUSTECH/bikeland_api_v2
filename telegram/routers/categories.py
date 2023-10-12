from aiogram import Router, F
from aiogram.types import Message
from telegram.services import categories_service
from telegram.btn_names import WelcomeBtnNames

router = Router()

@router.message(F.text == WelcomeBtnNames.BIKE.value)
async def get_list_of_categories(message: Message) -> None:
    await categories_service.get_list_of_motorbike_categories(message=message)



@router.message(F.text == WelcomeBtnNames.EQUIPS.value)
async def get_list_of_categories(message: Message) -> None:
    await categories_service.get_list_of_equips(message)







