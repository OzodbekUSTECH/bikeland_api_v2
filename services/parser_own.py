from schemas.products import CreateProductMediaGroup
from schemas.blogs import CreateBlogMediaGroup
import models
from database import uow
from utils.parser_2 import ParserHandlerSecond
from utils.media_handler import MediaHandler

class ParserService:

    async def parse_own_products(self):
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

    async def parse_own_blogs(self):
        async with uow:
            blogs = await ParserHandlerSecond.get_all_data_by_url(ParserHandlerSecond.blogs_url)
            for blog in blogs:
                blog_model = await ParserHandlerSecond.create_blog_model(blog)

                created_blog: models.Blog = await uow.blogs.create(blog_model.model_dump())

                if blog_model.photos:
                    filenames = await MediaHandler.save_media_from_url(blog_model.photos, MediaHandler.blogs_media_dir)
                    await uow.product_media_groups.bulk_create(
                        data_list=[CreateBlogMediaGroup(
                            blog_id=created_blog.id,
                            filename=filename
                        ).model_dump() for filename in filenames]
                    )

            await uow.commit()
            
    async def parse_own_categories(self):
        async with uow:
            categories = await ParserHandlerSecond.get_all_data_by_url(ParserHandlerSecond.categories_url)
        
            for category in categories:
                category_model = await ParserHandlerSecond.create_category_model(category)
                await uow.categories.create(category_model.model_dump())

            await uow.commit()

    async def parse_own_sub_categories(self):
        async with uow:
            sub_categories = await ParserHandlerSecond.get_all_data_by_url(ParserHandlerSecond.sub_categories_url)
            for sub_category in sub_categories:
                sub_category_model = await ParserHandlerSecond.create_sub_category_model(sub_category)
                await uow.sub_categories.create(sub_category_model.model_dump())

            await uow.commit()

    async def parse_own_brands(self):
        async with uow:
            brands = await ParserHandlerSecond.get_all_data_by_url(ParserHandlerSecond.brands_url)
            for brand in brands:
                brand_model = await ParserHandlerSecond.create_brand_model(brand)
                await uow.brands.create(brand_model.model_dump())

            await uow.commit()


    async def change_the_order_of_photos(self):
        async with uow:
            main_products: list[models.Product] = await uow.products.get_all_without_pagination()
            add_products: list[models.Product] = await uow.products.get_all_without_pagination()
            for main_product, add_product in zip(main_products, add_products):
                for main_photo, add_photo in zip(main_product.photos, add_product.photos[::-1]):
                    main_photo.filename = add_photo.filename

            await uow.commit()



parser_service = ParserService()

