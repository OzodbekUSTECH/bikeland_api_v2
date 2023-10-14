from schemas.resource_catalog.delivery import CreateDeliverySchema, UpdateDeliverySchema, CreateDeliveryMediaSchema
import models
from repositories import paginate
from database import UnitOfWork
from utils.media_handler import MediaHandler
from fastapi import UploadFile
class DeliveryService:
    
    def __init__(self):
        self.uow = UnitOfWork()

    async def create_delivery(self, delivery_data: CreateDeliverySchema) -> models.Delivery:
        async with self.uow:
            delivery = await self.uow.delivery.create(delivery_data.model_dump())
            await self.uow.commit()
            return delivery
        
    async def create_delivery_media(self, photos: list[UploadFile]) -> None:
        filenames = await MediaHandler.save_media(photos, MediaHandler.delivery_media_dir)
        await self.uow.delivery_media.bulk_create(
            data_list=[CreateDeliveryMediaSchema(filename=filename).model_dump() for filename in filenames] 
        )
        await self.uow.commit()

    async def get_deliveries(self) -> list[models.Delivery]:
        async with self.uow:
            return await self.uow.delivery.get_all()
        
    async def get_delivery_media(self, params, no_pagination: bool) -> list[models.DeliveryMedia]:
        async with self.uow:
            instances = await self.uow.delivery_media.get_all_without_pagination(reverse=True)
            if no_pagination:
                return instances
            return paginate(instances, params)
        
    async def update_delivery(self, id: int, delivery_data: UpdateDeliverySchema) -> models.Delivery:
        async with self.uow:
            delivery: models.Delivery = await self.uow.delivery.get_by_id(id)
            await self.uow.delivery.update(delivery.id, delivery_data.model_dump())
            await self.uow.commit()
            return delivery
        
    async def delete_delivery(self, id: int) -> models.Delivery:
        async with self.uow:
            delivery: models.Delivery = await self.uow.delivery.get_by_id(id)
            await self.uow.delivery.delete(delivery.id)
            await self.uow.commit()
            return delivery

    async def delete_delivery_media(self, id: int) -> models.DeliveryMedia:
        async with self.uow:
            delivery_media: models.DeliveryMedia = await self.uow.delivery_media.get_by_id(id)
            await self.uow.delivery_media.delete(delivery_media.id)
            await self.uow.commit()
            return delivery_media
        

delivery_service = DeliveryService()
        