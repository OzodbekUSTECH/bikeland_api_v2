from schemas.resource_catalog.delivery import CreateDeliverySchema, UpdateDeliverySchema, CreateDeliveryMediaSchema
import models
from repositories import paginate
from utils.media_handler import MediaHandler
from fastapi import UploadFile
class DeliveryService:
    
    async def create_delivery(self,uow, delivery_data: CreateDeliverySchema) -> models.Delivery:
        async with uow:
            delivery = await uow.delivery.create(delivery_data.model_dump())
            await uow.commit()
            return delivery
        
    async def create_delivery_media(self,uow, photos: list[UploadFile]) -> None:
        filenames = await MediaHandler.save_media(photos, MediaHandler.delivery_media_dir)
        await uow.delivery_media.bulk_create(
            data_list=[CreateDeliveryMediaSchema(filename=filename).model_dump() for filename in filenames] 
        )
        await uow.commit()

    async def get_deliveries(self, uow,) -> list[models.Delivery]:
        async with uow:
            return await uow.delivery.get_all()
        
    async def get_delivery_media(self,uow, params, no_pagination: bool) -> list[models.DeliveryMedia]:
        async with uow:
            instances = await uow.delivery_media.get_all_without_pagination(reverse=True)
            if no_pagination:
                return instances
            return paginate(instances, params)
        
    async def update_delivery(self,uow, id: int, delivery_data: UpdateDeliverySchema) -> models.Delivery:
        async with uow:
            delivery: models.Delivery = await uow.delivery.get_by_id(id)
            await uow.delivery.update(delivery.id, delivery_data.model_dump())
            await uow.commit()
            return delivery
        
    async def delete_delivery(self, uow,id: int) -> models.Delivery:
        async with uow:
            delivery: models.Delivery = await uow.delivery.get_by_id(id)
            await uow.delivery.delete(delivery.id)
            await uow.commit()
            return delivery

    async def delete_delivery_media(self,uow, id: int) -> models.DeliveryMedia:
        async with uow:
            delivery_media: models.DeliveryMedia = await uow.delivery_media.get_by_id(id)
            await uow.delivery_media.delete(delivery_media.id)
            await uow.commit()
            return delivery_media
        

delivery_service = DeliveryService()
        