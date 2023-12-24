from schemas.products import CreateProductMediaGroup
from schemas.blogs import CreateBlogMediaGroup
from schemas.waiting_lists import CreateWaitingListSchema, UpdateWaitingListSchema
import models
from utils.parser_2 import ParserHandlerSecond
from utils.parser import ParserHandler
from utils.media_handler import MediaHandler
from config_bot import send_message_to_tg_admins, bot
from services import products_service
from database import UnitOfWork

class ParserService:

    async def parse_own_products(self, uow):
        async with uow:
            products = await ParserHandlerSecond.get_all_data_by_url(ParserHandlerSecond.products_url)

            for product in products:
                product_model = await ParserHandlerSecond.create_product_model(product)

                saved_product: models.Product = await uow.products.create(product_model.model_dump())
                
                if product_model.photos:
                    filenames = await MediaHandler.save_media_from_url(product_model.photos, MediaHandler.products_media_dir)
                    await uow.product_media_groups.bulk_create(
                        data_list=[CreateProductMediaGroup(
                            product_id=saved_product.id,
                            filename=filename
                        ).model_dump() for filename in filenames]
                    )
                            
            await uow.commit()

    async def parse_own_blogs(self, uow):
        async with uow:
            blogs = await ParserHandlerSecond.get_all_data_by_url(ParserHandlerSecond.blogs_url)
            for blog in blogs:
                blog_model = await ParserHandlerSecond.create_blog_model(blog)

                created_blog: models.Blog = await uow.blogs.create(blog_model.model_dump())

                if blog_model.photos:
                    filenames = await MediaHandler.save_media_from_url(blog_model.photos, MediaHandler.blogs_media_dir)
                    await uow.blog_media_group.bulk_create(
                        data_list=[CreateBlogMediaGroup(
                            blog_id=created_blog.id,
                            filename=filename
                        ).model_dump() for filename in filenames]
                    )

            await uow.commit()

    async def parse_own_categories(self, uow):
        async with uow:
            categories = await ParserHandlerSecond.get_all_data_by_url(ParserHandlerSecond.categories_url)
        
            for category in categories:
                category_model = await ParserHandlerSecond.create_category_model(category)
                await uow.categories.create(category_model.model_dump())

            await uow.commit()

    async def parse_own_sub_categories(self, uow):
        async with uow:
            sub_categories = await ParserHandlerSecond.get_all_data_by_url(ParserHandlerSecond.sub_categories_url)
            for sub_category in sub_categories:
                sub_category_model = await ParserHandlerSecond.create_sub_category_model(sub_category)
                await uow.sub_categories.create(sub_category_model.model_dump())

            await uow.commit()

    async def parse_own_brands(self, uow):
        async with uow:
            brands = await ParserHandlerSecond.get_all_data_by_url(ParserHandlerSecond.brands_url)
            for brand in brands:
                brand_model = await ParserHandlerSecond.create_brand_model(brand)
                await uow.brands.create(brand_model.model_dump())

            await uow.commit()


    async def change_the_order_of_photos(self, uow):
        async with uow:
            main_products: list[models.Product] = await uow.products.get_all_without_pagination()
            add_products: list[models.Product] = await uow.products.get_all_without_pagination()
            for main_product, add_product in zip(main_products, add_products):
                for main_photo, add_photo in zip(main_product.photos, add_product.photos[::-1]):
                    main_photo.filename = add_photo.filename

            await uow.commit()

    ############################################
    async def check_products_from_1c(self):
        uow = UnitOfWork()
        await products_service.create_products()

        async with uow:
            waiting_dealers_id = []

            products = await uow.products.get_all_without_pagination()
            their_products = await ParserHandler.get_filtered_products()
            for product1 in products:
                for product2 in their_products:
                    # Проверяем, есть ли product1.key в их списке ключей
                    if 'keys' in product2 and product1.key in product2['keys']:
                        # Это тот нужный товар, добавьте здесь ваш код для обработки
                        has_changes = await ParserHandler.has_changes_in_columns_of_1C_products(
                            product1, product2
                        )
                        
                        if has_changes:
                            
                            product_dict = await ParserHandler.create_product_dict(product2)
                            updated_product: models.Product = await uow.products.update(product1.id, product_dict)
                            if updated_product.quantity >= updated_product.min_quantity:
                                product_in_waiting_list: models.WaitingList = await uow.waiting_lists.get_one_by(product_id=updated_product.id)
                                if product_in_waiting_list:
                                    await uow.waiting_lists.delete(product_in_waiting_list.id)
                            elif updated_product.quantity < updated_product.min_quantity:
                                # await self.inform_user_about_quantity_of_product(updated_product)
                                if updated_product.dealer_id:
                                    waiting_dealers_id.append(updated_product.dealer_id)

                                    waiting_list_product = await uow.waiting_lists.get_one_by(product_id=updated_product.id)
                                    if waiting_list_product:
                                        waiting_list_dict = UpdateWaitingListSchema(
                                            dealer_id=updated_product.dealer_id,
                                            product_id=updated_product.id
                                        ).model_dump()
                                        await uow.waiting_lists.update(waiting_list_product.id, waiting_list_dict)
                                    else:
                                        waiting_list_dict = CreateWaitingListSchema(
                                            dealer_id=updated_product.dealer_id,
                                            product_id=updated_product.id
                                        ).model_dump()
                                        await uow.waiting_lists.create(waiting_list_dict)
            
            await uow.commit()
        if waiting_list_dict:
            await self.inform_user_about_quantity_of_product(waiting_dealers_id)

    async def auto_delete_product(self):
        uow = UnitOfWork()
        async with uow:
            products = await uow.products.get_all_without_pagination()
            for product in products:
                their_product = await ParserHandler.get_by_key(product.key)
                if not their_product:
                    await uow.products.delete(product.id)
            
            await uow.commit()

        
            
    async def inform_user_about_quantity_of_product(self, dealers_id: list[int]):
            uow = UnitOfWork()
            async with uow:
                for dealer_id in dealers_id:
                    dealer: models.Dealer = await uow.dealers.get_by_id(dealer_id)

                    products_data = ""
                    for product in dealer.waiting_list:
                        products_data += (
                            f"- Название товара: {product.title_of_product}\n"
                            f"- Осталось на складе: {product.quantity}\n"
                            f"- Минимальное кол-во: {product.min_quantity}\n"
                            f"- Необходимое кол-во пополнить: {product.required_quantity}\n\n"
                        )    
                    
                    message_text = (
                        f"Здравствуйте {dealer.full_name}. Вас приветствует администратор Bikeland.Uz\n"
                        f"{products_data}"
                        f"Для стабильного потока продаж необходимо пополнить склад!"
                    )
                    if dealer.telegram_id:
                        await bot.send_message(chat_id=dealer.telegram_id, text=message_text)
                    else:
                        message_notification = (
                            f"Дилер {dealer.full_name} не зарегистрирован в боте и не может получать уведомления.\n"
                            f"Номер телефона дилера: {dealer.phone_number}\n"
                            "Для правильной работы уведомлений дилер должен перейти в бота @BikelandUz_bot и отправить свой контакт"
                        )
                        await send_message_to_tg_admins(message_notification)
                
parser_service = ParserService()

