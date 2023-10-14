from schemas.orders import CreateOrderSchema
from schemas.tgclients import CreateTgClientSchema
import models
from database import UnitOfWork
from services import forms_service
class OrdersService:

    def __init__(self):
        self.uow = UnitOfWork()


    async def _create_or_get_tg_client(self, phone_number: str) -> models.TgClient:
        tgclient: models.TgClient = await self.uow.tgclients.get_one_by_phone_number(phone_number)
        if not tgclient:
            tgclient: models.TgClient = await self.uow.tgclients.create(CreateTgClientSchema(
                phone_number=phone_number
            ).model_dump())
        
        return tgclient

    async def create_order(self, order_data: CreateOrderSchema) -> models.Order:
        order_dict = order_data.model_dump()
        async with self.uow:
            tgclient = await self._create_or_get_tg_client(order_data.phone_number)
            order_dict["tgclient_id"] = tgclient.id
            order = await self.uow.orders.create(order_dict)
            await forms_service._inform_tg_admins(order=order)
            await self.uow.commit()

            return order
        
    async def get_orders(self) -> list[models.Order]:
        async with self.uow:
            return await self.uow.orders.get_all(reverse=True)
        
    async def delete_order(self, id: int) -> models.Order:
        async with self.uow:
            order: models.Order = await self.uow.orders.get_by_id(id)
            await self.uow.orders.delete(order.id)
            await self.uow.commit()
            return order
        
orders_service = OrdersService()