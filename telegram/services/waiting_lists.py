from database import UnitOfWork
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from telegram.states import SenderStates 
import models
from config_bot import bot
from telegram.reply_kbs import rkbs_handler

class WaitingListsService:

    async def show_products_of_waiting_list(self, uow: UnitOfWork, message: Message) -> None:
        async with uow:
            dealer: models.Dealer = await uow.dealers.get_one_by(telegram_id=message.from_user.id)
            if dealer.waiting_list:
                products_data = ""
                for product in dealer.waiting_list:
                    products_data += (
                        f"- Название товара: {product.title_of_product}\n"
                        f"- Осталось на складе: {product.quantity}\n"
                        f"- Минимальное кол-во: {product.min_quantity}\n"
                        f"- Необходимое кол-во пополнить: {product.required_quantity}\n\n"
                    )
                message_text = (
                    "Список необходимых товаров:\n"
                    f"{products_data}"
                )

                await message.answer(message_text)

            else:
                await message.answer("Все ваши товары в достаточном количестве для успешной бесперебойной продажи")

waiting_lists_service = WaitingListsService()