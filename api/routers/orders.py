from fastapi import APIRouter
from services import orders_service
from repositories import Page
from schemas.orders import (
    CreateOrderSchema,
    
    OrderSchema,
)
from schemas import IdResponseSchema

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

@router.post('', response_model=IdResponseSchema)
async def create_order(
    order_data: CreateOrderSchema
):
    return await orders_service.create_order(order_data)

@router.get('', response_model=Page[OrderSchema])
async def get_orders():
    return await orders_service.get_orders()

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_order(id: int):
    return await orders_service.delete_order(id)