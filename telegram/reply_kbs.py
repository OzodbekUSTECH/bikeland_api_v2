from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from telegram.btn_names import WelcomeBtnNames
from config import settings
import models
class ReplyKeyboardsHandler:

    async def get_sender_contact(self):
        kbs = [
            [KeyboardButton(text="Отправить контакт", request_contact=True)]
        ]
        rkb_markup = ReplyKeyboardMarkup(
            keyboard=kbs,
            resize_keyboard=True,
            input_field_placeholder="Нажмите 'ОТПРАВИТЬ КОНТАКТ', чтобы зарегистрироваться!"
        )
                    
        return rkb_markup
    
    async def get_welcome_rkbs(self, tg_id: int, dealers_tg_id: list[int]):
        rkbs = [
            KeyboardButton(
                text=f"{btn_name.value}", 
            )
            for btn_name in WelcomeBtnNames
        ]

        if tg_id in settings.ADMIN_TG_IDS:
            rkbs = rkbs + [KeyboardButton(text="Сделать рассылку")]
        
        if tg_id in dealers_tg_id:
            rkbs = rkbs + [KeyboardButton(text="Список товаров")]
        row = []
        for i in range(0, len(rkbs), 2):
            if i + 1 < len(rkbs):
                row.append([rkbs[i], rkbs[i + 1]])
            else:
                row.append([rkbs[i]])

        rkb_markup = ReplyKeyboardMarkup(
            keyboard=row,
            resize_keyboard=True,
        )
        return rkb_markup
    
    async def get_cancel_sender_rkb(self):
        rkb = KeyboardButton(text="Отменить")

        rkb_markup = ReplyKeyboardMarkup(
            keyboard=[[rkb]],
            resize_keyboard=True,
        )
        return rkb_markup
    
    async def send_post_or_cancel(self):
        rkbs = [
            KeyboardButton(text="Отменить"),
            KeyboardButton(text="Отправить"),
        ]

        rkb_markup = ReplyKeyboardMarkup(
            keyboard=[rkbs],
            resize_keyboard=True,
        )
        return rkb_markup
    
    async def get_motorbikes_categories(self, categories: list[models.Category]):
        rkbs = [
            KeyboardButton(
                text=category.name
            ) for category in categories if category.name not in ["Двигатели", "Экип/Аксессуары/Запчасти"] 
        ]
        rkbs.append(KeyboardButton(text="Назад"))

        row = []
        for i in range(0, len(rkbs), 2):
            if i + 1 < len(rkbs):
                row.append([rkbs[i], rkbs[i + 1]])
            else:
                row.append([rkbs[i]])

        ikb_markup = ReplyKeyboardMarkup(
            keyboard=row,
            resize_keyboard=True,
        )

        return ikb_markup
    
    async def get_equips_rkbs(self, sub_categories: list[models.SubCategory]):
        rkbs = [
            KeyboardButton(
                text=sub_category.name
            ) for sub_category in sub_categories
        ]
        rkbs.append(KeyboardButton(text="Двигатели"))
        rkbs.append(KeyboardButton(text="Назад"))

        row = []
        for i in range(0, len(rkbs), 2):
            if i + 1 < len(rkbs):
                row.append([rkbs[i], rkbs[i + 1]])
            else:
                row.append([rkbs[i]])

        ikb_markup = ReplyKeyboardMarkup(
            keyboard=row,
            resize_keyboard=True,
        )

        return ikb_markup

    async def cancel_ordering_btn(self):
        rkb = KeyboardButton(text="Отменить")

        rkb_markup = ReplyKeyboardMarkup(
            keyboard=[[rkb]],
            resize_keyboard=True,
        )
        return rkb_markup
    



rkbs_handler = ReplyKeyboardsHandler()