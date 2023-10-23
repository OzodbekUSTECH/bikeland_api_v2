from database import UnitOfWork
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from telegram.states import SenderStates 
import models
from config_bot import bot
from telegram.reply_kbs import rkbs_handler

class SenderService:
    

    async def create_post(self, message: Message, state: FSMContext):
        message_text = (
            "добавьте 1 фото или видео и текст к нему и нажмите «отправить»"
        )
        await state.set_state(SenderStates.create_post)
        rkb_markup = await rkbs_handler.get_cancel_sender_rkb()
        await message.answer(message_text, reply_markup=rkb_markup)

    async def save_post(self, message: Message, state: FSMContext):
        if message.text == "Отменить":
            await state.clear()
            uow = UnitOfWork()
            async with uow:
                dealers: list[models.Dealer] = await uow.dealers.get_all_without_pagination()
                dealers_tg_id = [dealer.telegram_id for dealer in dealers if dealer.telegram_id]
                rkb_markup = await rkbs_handler.get_welcome_rkbs(tg_id=message.from_user.id, dealers_tg_id=dealers_tg_id)
                await message.answer("Отменено", reply_markup=rkb_markup)
        else:
            if message.photo:
                await state.update_data(photo=message.photo[-1].file_id, caption = message.caption)
            elif message.video:
                await state.update_data(video = message.video.file_id, caption = message.caption)
            else:
                await state.update_data(caption = message.text)

            message_text = (
                "Отправляем?"
            )
            
            rkb_markup = await rkbs_handler.send_post_or_cancel()
            await message.answer(message_text, reply_markup=rkb_markup)
            await state.set_state(SenderStates.is_done)

    async def send_or_cancel_sender(self, message: Message, state: FSMContext, uow: UnitOfWork):
        if message.text == "Отменить":
            await state.clear()
            dealers: list[models.Dealer] = await uow.dealers.get_all_without_pagination()
            dealers_tg_id = [dealer.telegram_id for dealer in dealers if dealer.telegram_id]
            rkb_markup = await rkbs_handler.get_welcome_rkbs(tg_id=message.from_user.id, dealers_tg_id=dealers_tg_id)
            await message.answer("Отменено", reply_markup=rkb_markup)
        else:
            data = await state.get_data()
            photo = data.get("photo", None)
            video = data.get("video", None)
            caption = data.get("caption", None)
            tg_clients: list[models.TgClient] = await uow.tgclients.get_all_without_pagination()
            for client in tg_clients:
                if client.telegram_id:
                    if photo:
                        await bot.send_photo(chat_id=client.telegram_id, photo=photo, caption=caption)
                    elif video:
                        await bot.send_video(chat_id=client.telegram_id, video=video, caption=caption)
                    else:
                        await bot.send_message(chat_id=client.telegram_id, text=caption)
            dealers: list[models.Dealer] = await uow.dealers.get_all_without_pagination()
            dealers_tg_id = [dealer.telegram_id for dealer in dealers if dealer.telegram_id]
            rkb_markup = await rkbs_handler.get_welcome_rkbs(message.from_user.id, dealers_tg_id)
            await message.answer("рассылка прошла успешно", reply_markup=rkb_markup)
            await state.clear()

sender_service = SenderService()