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

@router.post('', response_model=IdResponseSchema)
async def create_delivery(
    delivery_data: CreateDeliverySchema
):
    return await delivery_service.create_delivery(delivery_data)

@router.post('/media')
async def create_delivery_media(
    photos: list[UploadFile]
):
    return await delivery_service.create_delivery_media(photos)

@router.get('/', response_model=Page[DeliverySchema])
async def get_deliveries():
    return await delivery_service.get_deliveries()

@router.get('/media', response_model=Page[DeliveryMediaSchema] | list[DeliveryMediaSchema])
async def get_all_delivery_media(params: Params = Depends(), no_pagination: bool = True):
    return await delivery_service.get_delivery_media(params, no_pagination)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_delivery(
    id: int,
    delivery_data: UpdateDeliverySchema
):
    return await delivery_service.update_delivery(id, delivery_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_delivery(id: int):
    return await delivery_service.delete_delivery(id)

@router.delete('/media/{id}', response_model=IdResponseSchema)
async def delete_delivery_media(id: int):
    return await delivery_service.delete_delivery_media(id)