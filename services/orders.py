from schemas.orders import CreateOrderSchema, CreateCustomOrderBasketSchema
from schemas.tgclients import CreateTgClientSchema
import models
from database import UnitOfWork
from services import forms_service
class OrdersService:

    async def _create_or_get_tg_client(self,uow, phone_number: str) -> models.TgClient:
        tgclient: models.TgClient = await uow.tgclients.get_one_by_phone_number(phone_number)
        if not tgclient:
            tgclient: models.TgClient = await uow.tgclients.create(CreateTgClientSchema(
                phone_number=phone_number
            ).model_dump())
        
        return tgclient

    async def create_order(self,uow: UnitOfWork, order_data: CreateOrderSchema) -> models.Order:
        order_dict = order_data.model_dump()
        async with uow:
            tgclient = await self._create_or_get_tg_client(uow, order_data.phone_number)
            order: models.Order = await uow.orders.create(order_dict)
            await uow.orders_basket.bulk_create(
                data_list=[CreateCustomOrderBasketSchema(
                    order_id=order.id,
                    product_id=data.product_id,
                    quantity=data.quantity,
                    option_ids=data.option_ids,
                    tgclient_id= tgclient.id
                ).model_dump() for data in order_data.basket]
            )
            await uow.commit()

            order = await uow.orders.get_by_id(order.id)
            
            await forms_service._inform_tg_admins(uow, order=order)

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