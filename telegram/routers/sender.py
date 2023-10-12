from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from telegram.services import sender_service
from telegram.states import SenderStates 

router = Router()

@router.message(F.text == "Сделать рассылку")
async def create_post(message: Message, state: FSMContext):
    await sender_service.create_post(message, state)

@router.message(SenderStates.create_post)
async def save_post(message: Message, state: FSMContext):
    await sender_service.save_post(message, state)


@router.message(SenderStates.is_done)
async def send_or_cancel_sender(message: Message, state: FSMContext):
    await sender_service.send_or_cancel_sender(message, state)