from schemas.orders import CreateOrderSchema
from schemas.tgclients import CreateTgClientSchema
import models
from services import forms_service
class OrdersService:

    async def _create_or_get_tg_client(self,uow, phone_number: str) -> models.TgClient:
        tgclient: models.TgClient = await uow.tgclients.get_one_by_phone_number(phone_number)
        if not tgclient:
            tgclient: models.TgClient = await uow.tgclients.create(CreateTgClientSchema(
                phone_number=phone_number
            ).model_dump())
        
        return tgclient

    async def create_order(self,uow, order_data: CreateOrderSchema) -> models.Order:
        order_dict = order_data.model_dump()
        async with uow:
            tgclient = await self._create_or_get_tg_client(uow, order_data.phone_number)
            order_dict["tgclient_id"] = tgclient.id
            order = await uow.orders.create(order_dict)
            await forms_service._inform_tg_admins(order=order)
            await uow.commit()

            return order
        
    async def get_orders(self, uow,) -> list[models.Order]:
        async with uow:
            return await uow.orders.get_all(reverse=True)
        
    async def delete_order(self,uow, id: int) -> models.Order:
        async with uow:
            order: models.Order = await uow.orders.get_by_id(id)
            await uow.orders.delete(order.id)
            await uow.commit()
            return order
        
orders_service = OrdersService()