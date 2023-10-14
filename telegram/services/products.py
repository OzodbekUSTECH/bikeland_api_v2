from database import uow
from aiogram.types import Message, CallbackQuery
import models
from telegram.reply_kbs import rkbs_handler
from telegram.inline_kbs import ikbs_handler
from config_bot import bot
from config import settings
from datetime import datetime
from telegram.btn_names import SorterBtnNames
from telegram.utils.filter_products import FilterProductsHandler
from aiogram.types import InlineKeyboardMarkup
from aiogram.types.input_media_photo import InputMediaPhoto
from telegram.call_backs import ChangeBrandCallBackData, SorterCallBackData

class ProductsService:

    def __init__(self):
       
        self.cache_categories = []
        self.cache_sub_categories = []
        self.message_exceptions = ["Назад", "Корзина", "/start", "Отменить", "Сделать рассылку"]

    async def _notify_admins_tg(self, message: Message):
            telegram_client: models.TgClient = await uow.tgclients.get_one_by(telegram_id=message.from_user.id)
            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            message_text = (
                    "Поступило новое сообщение из бота:\n"
                    f"Дата: {timestamp}\n"
                    f"Номер пользователя: {telegram_client.phone_number}\n"
                    f"Сообщение: {message.text}"
                )
            for admin_tg_id in settings.ADMIN_TG_IDS:

                await bot.send_message(chat_id=admin_tg_id, text=message_text)

    async def get_products(self, message: Message) -> None:
        async with uow: 
            if not self.cache_categories or not self.cache_sub_categories:
                self.cache_categories = [category.name for category in await uow.categories.get_all_without_pagination()]
                self.cache_sub_categories = [sub_category.name for sub_category in await uow.sub_categories.get_all_without_pagination()]
            if message.text == "Назад":
                rkb_markup = await rkbs_handler.get_welcome_rkbs(message.from_user.id)
                return await message.answer("Выберите категорию товаров", reply_markup=rkb_markup)
            
            if message.text not in self.cache_categories and message.text not in self.cache_sub_categories and message.text not in self.message_exceptions and not message.contact:
                return await self._notify_admins_tg(message)
            
            if message.text in self.cache_categories:
                category: models.Category = await uow.categories.get_one_by(name=message.text)
                await self.paginate_products(
                    message=message,
                    category_id=category.id,
                )

            elif message.text in self.cache_sub_categories:
                sub_category: models.SubCategory = await uow.sub_categories.get_one_by(name=message.text)
                
                await self.paginate_products(
                    message=message,
                    sub_category_id=sub_category.id
                )

       

            
           
    async def paginate_products(
            self,
            message: Message = None,
            query: CallbackQuery = None,
            category_id: int = None,
            sub_category_id: int = None,
            current_page: int = 1,
            sort_by: str = SorterBtnNames.DEFAULT.name,
            brand_name: str = "Все"
    ) -> None:
        async with uow:
            if category_id:
                products: list[models.Product] = await uow.products.get_all_by(category_id=category_id, status_id=settings.PUBLISHED_STATUS_ID)

            else:
                products: list[models.Product] = await uow.products.get_all_by(sub_category_id=sub_category_id, status_id=settings.PUBLISHED_STATUS_ID)

            products = await FilterProductsHandler.filter_products(
                sort_by=sort_by,
                products=products,
            )
            
            
            
            if brand_name != "Все" and brand_name != None:
                    products = [product for product in products if product.brand and product.brand.name == brand_name]

            if not products:
                return await message.answer("К сожалению, товаров временно нет. Приносим свои извенения за неудобства...")
            total_pages = len(products)
            if current_page > total_pages:
                current_page = 1
            elif current_page == 0:
                current_page = total_pages
            product = products[current_page - 1]

            ikb_markup = await ikbs_handler.get_pagination_ikbs(
                total_pages=total_pages,
                product= product,
                category_id=category_id,
                sub_category_id=sub_category_id,
                current_page=current_page,
                sort_by=sort_by,
                brand_name = brand_name
            )

            await self._show_product(
                message=message,
                query=query,
                product = product,
                ikb_markup=ikb_markup,
            )


    async def _show_product(
            self,
            message: Message | None,
            query: CallbackQuery | None,
            product: models.Product,
            ikb_markup: InlineKeyboardMarkup,
    ) -> None:
        photo_url = "https://files.glotr.uz/company/000/002/656/logo/14143547079268-4ae5e4c10cea0e50e657c885a657701e.jpg?_=gzauc"
        if product.photos:
            photo_url = product.photos[0].photo_url
            
        # #use 2 spaces to show space in tg
        weight_text = f"• Вес: {product.weight}\n" if product.weight else ""
        sizes_text = f"• Размеры Д*Ш*В:  {product.sizes}\n" if product.sizes else ""
        power_text = f"• Мощность:  {product.max_power}\n" if product.max_power else ""
        max_speed_text = f"• Максимальная скорость:  {product.max_speed}\n" if product.max_speed else ""
        fuel_tank_volume_text = f"• Объем топливного бака:  {product.fuel_tank_volume}\n" if product.fuel_tank_volume else ""
        fuel_consumption_text = f"• Расход топлива:  {product.fuel_consumption}\n" if product.fuel_consumption else ""
        link_text = f"Ссылка на обзор товара: <a href='{product.video_link}'>Открыть</a>\n" if product.video_link else ""
        

        caption_text = (
            f"Название товара:  {product.title}\n\n"
            f"{weight_text}"
            f"{sizes_text}"
            f"{power_text}"
            f"{max_speed_text}"
            f"{fuel_tank_volume_text}"
            f"{fuel_consumption_text}"
            f"Цена:  {product.uzb_price:,}".replace(',', ' ') + " сум\n"  # Заменяем запятые на пробелы
            f"Наш канал: @BikelandUz\n"
            f"{link_text}"       
        )
        
        
       
        if query is not None:
            await query.message.edit_media(
                media=InputMediaPhoto(media=photo_url, caption=caption_text, parse_mode="HTML")
            )
            await query.message.edit_reply_markup(reply_markup=ikb_markup)
        else:
            await message.answer_photo(photo_url, caption_text, reply_markup=ikb_markup, parse_mode="HTML")
    async def change_brand(
            self, 
            query: CallbackQuery,
            callback_data: ChangeBrandCallBackData,
    ):
        # async with uow:
            if callback_data.category_id:
                 products: list[models.Product] = await uow.products.get_all_by(category_id=callback_data.category_id, status_id=settings.PUBLISHED_STATUS_ID)

            else:
                products: list[models.Product] = await uow.products.get_all_by(sub_category_id=callback_data.sub_category_id, status_id=settings.PUBLISHED_STATUS_ID)

            products = list(filter(lambda item: item.quantity > 0, products))
            
            ikb_markup = await ikbs_handler.get_brands_ikbs(
                products=products,
                category_id=callback_data.category_id,
                sub_category_id=callback_data.sub_category_id,
                sort_by=callback_data.sort_by,
            )

            await query.message.edit_reply_markup(reply_markup=ikb_markup)
    
    async def sort_products(
            self, 
            query: CallbackQuery,
            callback_data: SorterCallBackData
    ):
        ikb_markup = await ikbs_handler.get_sorter_ikbs(
            category_id=callback_data.category_id,
            sub_category_id=callback_data.sub_category_id,
            sort_by=callback_data.sort_by,
            brand_name=callback_data.brand_name,
        )
        await query.message.edit_reply_markup(reply_markup=ikb_markup)


products_service = ProductsService()