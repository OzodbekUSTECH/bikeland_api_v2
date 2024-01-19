from schemas.product_options import CreateMultipleProductOptions, CreateProductOptionSchema, UpdateProductOptionSchema
import models
from database import UnitOfWork

class ProductOptionsService:

    async def create_multiple_product_options(self,uow: UnitOfWork,  product_id: int, options: list[CreateMultipleProductOptions]) -> None:
        async with uow:
            product: models.Product = await uow.products.get_by_id(product_id)
            await uow.product_options.bulk_create(
                data_list=[CreateProductOptionSchema(
                    product_id=product.id,
                    name= option.name,
                    price = option.price
                ).model_dump() for option in options]
            )
            await uow.commit()

    async def create_product_option(self, uow: UnitOfWork, option_data: CreateProductOptionSchema) -> models.ProductOption:
        async with uow:
            option = await uow.product_options.create(option_data.model_dump())
            await uow.commit()
            return option
        
    async def update_product_option(self, uow: UnitOfWork, id: int, option_data: UpdateProductOptionSchema) -> models.ProductOption:
        async with uow:
            option: models.ProductOption = await uow.product_options.get_by_id(id)
            await uow.product_options.update(option.id, option_data.model_dump())
            await uow.commit()
            return option
        
    async def delete_product_option(self, uow: UnitOfWork, id: int) -> models.ProductOption:
        async with uow:
            option: models.ProductOption = await uow.product_options.get_by_id(id)
            await uow.product_options.delete(option.id)
            await uow.commit()
            return option
        

product_options_service = ProductOptionsService()