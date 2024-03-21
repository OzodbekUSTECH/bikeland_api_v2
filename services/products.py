from schemas.products import UpdateProductSchema, CreateProductMediaGroup
import models
from utils.parser import ParserHandler
from utils.media_handler import MediaHandler
from fastapi import UploadFile
from config import settings
from utils.filters.filter_products import FilterProductsParams
from repositories import paginate, pagination_params
from database import UnitOfWork
from collections import Counter
import os


class ProductsService:
    
    # async def duplicates(self) -> None:
    #     async with uow:
    #         our_products = await uow.products.get_all_without_pagination()
    #         # filtered_products: list[dict] = await ParserHandler.get_filtered_products()
    #         # print(len(filtered_products))
            
    #         # Создайте множество для хранения уникальных titles
    #         unique_titles = set()
            
    #         # Создайте список для повторяющихся titles
    #         duplicate_titles = []
            
    #         for product in our_products:
    #             title = product.title
                
    #             # Если title уже существует в множестве, это повтор
    #             if title in unique_titles:
    #                 duplicate_titles.append(title)
    #             else:
    #                 unique_titles.add(title)
            
    #         print("Повторяющиеся titles:", duplicate_titles)

    async def get_product_1c_by_key(self, key):
        products_1c = await ParserHandler.get_by_key(key)
        return products_1c


    async def create_products(self) -> None:
        uow = UnitOfWork()
        async with uow:
            our_products = await uow.products.get_all_without_pagination()
            filtered_products: list[dict] = await ParserHandler.get_filtered_products()
            # print(len(filtered_products))
            # print(len(our_products))
            if len(our_products) != len(filtered_products):
                data_list = []
                for product in filtered_products:
                    naimenovanie = product.get("naimenovanie")
                    
                    our_product: models.Product = await uow.products.get_one_by(title=naimenovanie)
                    if not our_product:
                        product_dict = await ParserHandler.create_product_dict(
                            product
                        )
                        product_dict["status_id"] = settings.NOT_FILLED_IN_STATUS_ID
                        data_list.append(product_dict)

                await uow.products.bulk_create(data_list)
                await uow.commit()

    async def create_media_group(self,uow, product_id: int, media_group: list[UploadFile]) -> None:
        filenames = await MediaHandler.save_media(media_group, MediaHandler.products_media_dir)
        async with uow:
            product: models.Product = await uow.products.get_by_id(product_id)
            await uow.product_media_groups.bulk_create(
                data_list=[CreateProductMediaGroup(
                    product_id=product.id,
                    filename=filename
                ).model_dump() for filename in filenames]
            )
            await uow.commit()



    async def get_products(
            self,
            uow: UnitOfWork,
            filter_params: FilterProductsParams,
            pagination: pagination_params
        ) -> list[models.Product]:
        async with uow:
            products = await uow.products.filter_products(params=filter_params)
            # if filter_params.with_pagination:
            #     return paginate(products, pagination)
            # return products
            # products: list[models.Product] = await uow.products.get_all_without_pagination()
            # filtered_products: list[models.Product] = await filter_params.get_filtered_items(products)
            # filtered_products = await filter_params.sort_products(filtered_products)

            if filter_params.with_pagination:
                return paginate(products, pagination)
            return products
        
    async def get_product_by_id(self,uow, id: int) -> models.Product:
        async with uow:
            product: models.Product = await uow.products.get_by_id(id)
            await product.increase_view()
            await uow.commit()
            return product
        
    async def update_product(
            self,
            uow: UnitOfWork,
            is_to_publish: bool,
            id: int, 
            product_data: UpdateProductSchema
        ) -> models.Product:
        product_dict = product_data.model_dump()
        if is_to_publish:
            product_dict["status_id"] = settings.PUBLISHED_STATUS_ID
        else:
            product_dict["status_id"] = settings.ARCHIVED_STATUS_ID
        async with uow:
            product: models.Product = await uow.products.get_by_id(id)

            await uow.products.update(product.id, product_dict)
            await uow.commit()
            return product
        
    async def send_product_to_archive(self, uow,id: int) -> models.Product:
        async with uow:
            product: models.Product = await uow.products.get_by_id(id)
            product.status_id = settings.ARCHIVED_STATUS_ID
            await uow.commit()
            return product
        
    async def delete_media(self, uow, id: int) -> models.ProductMediaGroup:
        async with uow:
            product_media: models.ProductMediaGroup = await uow.product_media_groups.get_by_id(id)
            
            # Полный путь к файлу
            file_path = os.path.join('media', 'products', product_media.filename)
            
            # Удаление файла из файловой системы
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Удаление записи из базы данных
            await uow.product_media_groups.delete(product_media.id)
            await uow.commit()
            
            return product_media
            
    

    ################################
    async def check_products_from_1c(self,uow,):
        async with uow:
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
                            updated_product = await uow.products.update(product1.id, product_dict)
                            await uow.commit()
                            # await self.inform_user_about_quantity_of_product(updated_product)

    #########################################
    async def get_only_duplicates(self, uow: UnitOfWork):
        async with uow:
            products = await uow.products.get_all_without_pagination()

            # Получаем Counter для подсчета количества вхождений каждого title
            title_counter = Counter(product.title for product in products)

            # Фильтруем только те продукты, у которых количество вхождений title больше 1
            duplicate_products = [product for product in products if title_counter[product.title] > 1]
            print(duplicate_products)
            return duplicate_products
        

    async def delete_product(self, uow: UnitOfWork, id):
        async with uow:
            await uow.products.delete(id)

            await uow.commit()



products_service = ProductsService()