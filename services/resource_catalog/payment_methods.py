from schemas.resource_catalog.payment_methods import CreatePaymentMethodSchema, UpdatePaymentMethodSchema
import models
from database import UnitOfWork
from utils.media_handler import MediaHandler

class PaymentMethodsService:

    def __init__(self):
        self.uow = UnitOfWork()

    async def create_payment_method(self, payment_data: CreatePaymentMethodSchema) -> models.PaymentMethod:
        payment_dict = payment_data.model_dump()
        filename = await MediaHandler.save_media(payment_data.filename, MediaHandler.payment_methods_media_dir)
        payment_dict["filename"] = filename
        async with self.uow:
            payment_method = await self.uow.payment_methods.create(payment_dict)
            await self.uow.commit()
            return payment_method
        

    async def get_payment_methods(self) -> list[models.PaymentMethod]:
        async with self.uow:
            return await self.uow.payment_methods.get_all()
        
    async def get_payment_method_by_id(self, id: int) -> models.PaymentMethod:
        async with self.uow:
            return await self.uow.payment_methods.get_by_id(id)
        
    async def update_payment_method(self, id: int, payment_data: UpdatePaymentMethodSchema) -> models.PaymentMethod:
        payment_dict = payment_data.model_dump(exclude={"filename"})
        if payment_data.filename is not None:
            filename = await MediaHandler.save_media(payment_data.filename, MediaHandler.payment_methods_media_dir)
            payment_dict["filename"] = filename
        async with self.uow:
            payment_method: models.PaymentMethod = await self.uow.payment_methods.get_by_id(id)
            await self.uow.payment_methods.update(payment_method.id, payment_dict)
            await self.uow.commit()
            return payment_method
        
    async def delete_payment_method(self, id: int) -> models.PaymentMethod:
        async with self.uow:
            payment_method: models.PaymentMethod = await self.uow.payment_methods.get_by_id(id)
            await self.uow.payment_methods.delete(payment_method.id)
            await self.uow.commit()
            return payment_method
        
payment_methods_service = PaymentMethodsService()
