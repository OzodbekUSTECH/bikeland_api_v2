from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from telegram.services import waiting_lists_service
from telegram.states import SenderStates 
from database import UnitOfWork
router = Router()

@router.message(F.text == "Список товаров")
async def create_post(message: Message, uow = UnitOfWork()):
    await waiting_lists_service.show_products_of_waiting_list(uow, message)