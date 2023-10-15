from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from telegram.services import welcome_service
from telegram.states import WelcomeStates
from database import UnitOfWork

router = Router()

@router.message(F.text == "/start")
async def ask_for_contacts(message: Message, state: FSMContext, uow = UnitOfWork()):
    async with uow:
        await welcome_service.ask_for_contacts(message, state, uow)

# @router.message(F.photo)
# async def get_test(message: Message):
#     await welcome_service.upload_photos(message)


@router.message(WelcomeStates.contact)
async def register_client(message: Message, state: FSMContext, uow = UnitOfWork()) -> None:
    
    await welcome_service.register_tg_client(message, state, uow)