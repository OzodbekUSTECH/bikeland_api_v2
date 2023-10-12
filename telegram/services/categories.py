from database import uow
from aiogram.types import Message, CallbackQuery
from telegram.reply_kbs import rkbs_handler







class CategoriesService:
    
    async def get_list_of_motorbike_categories(self, message: Message = None) -> None:
        async with uow:
            categories = await uow.categories.get_all_without_pagination()
            rkbs = await rkbs_handler.get_motorbikes_categories(categories)
            message_text = "Выберите желаемый товар"
            await message.answer(message_text, reply_markup=rkbs)

    async def get_list_of_equips(self, message: Message):
        async with uow:
            sub_categories = await uow.sub_categories.get_all_without_pagination()
            rkb_markup = await rkbs_handler.get_equips_rkbs(sub_categories)
            message_text = "Выберите желаемый товар"
            await message.answer(message_text, reply_markup=rkb_markup)




categories_service = CategoriesService()