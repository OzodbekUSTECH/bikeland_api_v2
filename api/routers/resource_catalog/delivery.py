from fastapi import APIRouter, Depends, UploadFile
from services import delivery_service
from repositories import Page
from schemas.resource_catalog.delivery import (
    CreateDeliverySchema,
    UpdateDeliverySchema,
    DeliverySchema,

    DeliveryMediaSchema
)
from schemas import IdResponseSchema
from fastapi_pagination import Params

router = APIRouter(
    prefix="/delivery",
    tags=["Delivery and Delivery Media"],
)

from database import uow_dep

@router.post('', response_model=IdResponseSchema)
async def create_delivery(
    uow: uow_dep,
    delivery_data: CreateDeliverySchema
):
    return await delivery_service.create_delivery(uow, delivery_data)

@router.post('/media')
async def create_delivery_media(
    photos: list[UploadFile],
    uow: uow_dep,
):
    return await delivery_service.create_delivery_media(uow, photos)

@router.get('/', response_model=Page[DeliverySchema])
async def get_deliveries(uow: uow_dep,):
    return await delivery_service.get_deliveries(uow)

@router.get('/media', response_model=Page[DeliveryMediaSchema] | list[DeliveryMediaSchema])
async def get_all_delivery_media(uow: uow_dep,params: Params = Depends(), no_pagination: bool = True):
    return await delivery_service.get_delivery_media(uow, params, no_pagination)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_delivery(
    id: int,
    uow: uow_dep,
    delivery_data: UpdateDeliverySchema
):
    return await delivery_service.update_delivery(uow, id, delivery_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_delivery(uow: uow_dep, id: int):
    return await delivery_service.delete_delivery(uow, id)

@router.delete('/media/{id}', response_model=IdResponseSchema)
async def delete_delivery_media(uow: uow_dep, id: int):
    return await delivery_service.delete_delivery_media(uow, id)