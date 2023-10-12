from database import uow
from aiogram.types import Message, CallbackQuery
import models
from aiogram.types.input_media_photo import InputMediaPhoto
from telegram.inline_kbs import ikbs_handler
from aiogram.types import InlineKeyboardMarkup

class BasketService:

    async def show_basket(self, message: Message):
        await self.paginate_basket(message=message)

    async def paginate_basket(
            self,
            message: Message = None,
            query: CallbackQuery = None,
            current_page: int = 1,
    ):
        async with uow:
            if message:
                telegram_id = message.from_user.id
            else:
                telegram_id = query.from_user.id
            
                   
            client: models.TgClient = await uow.tgclients.get_one_by(telegram_id=telegram_id)
            orders: list[models.Order] = client.orders
            if not orders:
                return await message.answer("Пока вы ничего не заказали. Чтобы выбрать технику перейдите в каталог")
            sort_key = lambda order: order.id
            orders = sorted(
                orders,
                key=sort_key,
                reverse=True
            ) 

            total_pages = len(orders)
            if current_page > total_pages:
                current_page = 1
            elif current_page == 0:
                current_page = total_pages

            order: models.Order = orders[current_page - 1]
            product = order.product

            ikb_markup = await ikbs_handler.get_basket_pagination_ikbs(
                total_pages=total_pages,
                product= product,
                current_page=current_page,
                order_id = order.id
            )

            await self._show_product(
                message=message,
                query=query,
                order = order,
                product=product,
                ikb_markup=ikb_markup
            )

    async def _show_product(
            self,
            order: models.Order,
            product: models.Product,
            ikb_markup: InlineKeyboardMarkup,
            message: Message = None,
            query: CallbackQuery = None,
    ):
        photo_url = "https://files.glotr.uz/company/000/002/656/logo/14143547079268-4ae5e4c10cea0e50e657c885a657701e.jpg?_=gzauc"
        if product.photos:
            photo_url = product.photos[0].photo_url
            
        #use 2 spaces to show space in tg
        caption_text = (
            f"Номер заказа:  {order.id}\n"
            f"Название товара:  {product.title}\n\n"
            f"Количество:  {order.quantity}\n"
            f"Цена:  {order.price:,}".replace(',', ' ') + " сум\n"            
            f"Регион: {order.region}\n"
            f"Номер телефона:  {order.phone_number}\n"
            f"Имя:  {order.name}\n"
            f"Дата заказа:  {order.created_at}\n"
            f"Наш канал: @BikelandUz"
        )
      
        if message:
            await message.answer_photo(photo_url, caption_text, reply_markup=ikb_markup, parse_mode="HTML")
        else:
            await query.message.edit_media(
                media=InputMediaPhoto(media=photo_url, caption=caption_text, parse_mode="HTML")
            )
            await query.message.edit_reply_markup(reply_markup=ikb_markup)
        


basket_service = BasketService()