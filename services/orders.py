from schemas.orders import CreateOrderSchema
import models
from database import uow

class OrdersService:

    async def create_order(self, order_data: CreateOrderSchema) -> models.Order:
        async with uow:
            order = await uow.orders.create(order_data.model_dump())
            await uow.commit()
            return order
        
    async def get_orders(self) -> list[models.Order]:
        async with uow:
            return await uow.orders.get_all(reverse=True)
        
    async def delete_order(self, id: int) -> models.Order:
        async with uow:
            order: models.Order = await uow.orders.get_by_id(id)
            await uow.orders.delete(order.id)
            await uow.commit()
            return order
        
orders_service = OrdersService()