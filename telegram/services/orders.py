from database import uow
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from telegram.states import OrderStates
import models
import re

from config_bot import bot
from config import settings
from telegram.reply_kbs import rkbs_handler
from schemas.orders import CreateOrderSchema

class OrdersService:

    async def get_product_id(
            self, 
            query: CallbackQuery, 
            state: FSMContext,
            product_id: int
        ):
        await state.update_data(product_id=int(product_id))
        await state.set_state(OrderStates.region)
        message_text = (
            "Введите город, регион доставки.\n"
            "Пример: Ташкент, Бухара"
        )
        rkb = await rkbs_handler.cancel_ordering_btn()
        await query.message.answer(message_text, reply_markup=rkb)

    async def get_region(self, message: Message, state: FSMContext) -> None:
        await state.update_data(region = message.text)
        await state.set_state(OrderStates.name)
        message_text = (
            "Введите имя\n"
            "Пример: Тимур"
        )
        await message.answer(message_text)

    async def get_name(self, message: Message, state: FSMContext) -> None:
        await state.update_data(name = message.text)
        await state.set_state(OrderStates.phone_number)
        message_text = (
            "Введите номер телефона\n"
            "Пример: +998994567890"
        )
        await message.answer(message_text)

    async def get_phone_number(self, message: Message, state: FSMContext) -> None:
        phone_number_pattern = re.compile(r'^\+[0-9]+$')
        phone_number = message.text
        if phone_number_pattern.match(phone_number):
            await state.update_data(phone_number=phone_number)
            await state.set_state(OrderStates.quantity)
            message_text = (
                "Введите количество товаров\n"
                "Пример: 2"
            )
            await message.answer(message_text)
        else:
            await message.answer("Пожалуйста, введите корректный номер телефона, начиная с символа '+' и содержащий только цифры.")

    async def get_quantity_and_show_order_data(self, message: Message, state: FSMContext):
        if re.match(r"^\d+$", message.text):  # Проверяем, что введен текст состоит только из цифр
            quantity = int(message.text)
            if quantity < 1:
                return await message.answer(f"Вывведите число от 1 и не больше остатка")
            else:
                await state.update_data(quantity = quantity)
                await self.show_order_data(message, state)
        else:
            return await message.answer("Введите корректное количество")

    async def show_order_data(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        readable_data = await self._show_data(message, data, state)
        
        message_text = (
            "Ваш заказ принят, ожидайте. Скоро менеджер с вами свяжется\n\n"
            f"{readable_data}"
        )
        ikbs = await rkbs_handler.get_welcome_rkbs(tg_id=message.from_user.id)
        await message.answer(message_text, reply_markup=ikbs)

    async def _show_data(self, message: Message, data: dict, state: FSMContext):
        region = data.get('region', None)
        name = data.get('name', None)
        phone_number = data.get('phone_number', None)
        product_id = data.get('product_id', None)
        quantity = data.get('quantity', 1)
        
        async with uow:
            tgclient: models.TgClient = await uow.tgclients.get_one_by(telegram_id=message.from_user.id)

            order_dict = CreateOrderSchema(
                name=name,
                phone_number=phone_number,
                product_id=product_id,
                quantity=quantity,
                region=region,
                known_from="Телеграм бот",
            ).model_dump()
            order_dict["source"] = "Телеграм бот"
            order_dict["tgclient_id"] = tgclient.id
           
            order:models.Order = await uow.orders.create(order_dict)
            await uow.commit()
            await self.send_notification_to_admins_tg(order)
             
        unpacked_data = (
            f"Регион: {region}\n"
            f"Имя: {name}\n"
            f"Номер телефона: {phone_number}\n"
            f"Количество: {quantity}\n"
            f"Номер заказа: {order.id}\n"
            f"Ваши заказы хранятся в корзине"
        )
        await state.clear()
        
        return unpacked_data  


    async def send_notification_to_admins_tg(self, order: models.Order) -> None:
        
        message_text = (
                f"Заказ из телеграм бота\n\n"
                f"Дата время заказа: {order.created_at}\n"
                f"ID/Номер заказа: {order.id}\n"
                f"Имя: {order.name}\n"
                f"Номер телефона: {order.phone_number}\n"
                f"Название товара: {order.product.title}\n"
                f"Количество: {order.quantity}\n"
                f"Цена:  {order.price:,}".replace(',', ' ') + " сум\n"
                f"Регион {order.region}\n"
                # f"Узнал от: {order.known_from}\n"
            )
        product: models.Product = await uow.products.get_by_id(order.product_id)
        if product.sub_category:
            message_text +=(
                f"Категория: {product.sub_category.name}"
            )
        elif product.category:
            message_text +=(
                f"Категория: {product.category.name}"
            )
            for admin_tg_id in settings.ADMIN_TG_IDS:
                await bot.send_message(
                        chat_id=admin_tg_id,
                        text=message_text
                    )   

    async def cancel_ordering(self, message: Message, state: FSMContext) -> None:
        await state.clear()
        ikbs = await rkbs_handler.get_welcome_rkbs(tg_id=message.from_user.id)
        await message.answer("Оформление было отменено", reply_markup=ikbs)




orders_service = OrdersService()
