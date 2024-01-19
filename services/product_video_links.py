from schemas.product_video_links import CreateProductVideoLinkShema, UpdateProductVideoLinkSchema
import models
from database import UnitOfWork

class ProductVideoLinksService:

    async def create_product_video_link(self, uow: UnitOfWork, data: CreateProductVideoLinkShema) -> models.ProductVideoLink:
        async with uow:
            product: models.Product = await uow.products.get_by_id(data.product_id)
            
            product_video_link = await uow.product_video_links.create(data.model_dump())
            await uow.commit()
            return product_video_link
        
    async def update_product_video_link(self, uow: UnitOfWork, id: int, data: UpdateProductVideoLinkSchema) -> models.ProductVideoLink:
        async with uow:
            product_video_link: models.ProductVideoLink = await uow.product_video_links.get_by_id(id)
            product_video_link = await uow.product_video_links.update(product_video_link.id, data.model_dump())
            await uow.commit()
            return product_video_link
        
    async def delete_product_video_link(self, uow: UnitOfWork, id: int) -> models.ProductVideoLink:
        async with uow:
            product_video_link: models.ProductVideoLink = await uow.product_video_links.get_by_id(id)
            await uow.product_video_links.delete(product_video_link.id)
            await uow.commit()
            return product_video_link
        

    async def move_solo_video_link_to_multiple_links(self, uow: UnitOfWork):
        async with uow:
            products: list[models.Product] = await uow.products.get_all_with_video_link()
            for product in products:
                data = CreateProductVideoLinkShema(
                    product_id=product.id,
                    name="Обзор на YouTube",
                    link=product.video_link
                )
                await uow.product_video_links.create(data.model_dump())

            await uow.commit()
            return products
        

product_video_links_service = ProductVideoLinksService()