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
from database import uow_dep

@router.post('', response_model=IdResponseSchema)
async def create_order(
    order_data: CreateOrderSchema,
    uow: uow_dep,
):
    return await orders_service.create_order(uow, order_data)

@router.get('', response_model=Page[OrderSchema])
async def get_orders(uow: uow_dep,):
    return await orders_service.get_orders(uow)



@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_order(uow: uow_dep,id: int):
    return await orders_service.delete_order(uow, id)

