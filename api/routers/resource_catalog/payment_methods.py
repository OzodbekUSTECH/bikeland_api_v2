from fastapi import APIRouter, Depends, UploadFile, File, Form
from services import payment_methods_service
from repositories import Page
from schemas.resource_catalog.payment_methods import (
    CreatePaymentMethodSchema,
    UpdatePaymentMethodSchema,
    PaymentMethodSchema,
)
from schemas import IdResponseSchema

router = APIRouter(
    prefix="/payment-methods",
    tags=["Payment Methods (resource catalog)"],
)

from database import uow_dep

@router.post('', response_model=IdResponseSchema)
async def create_payment_method(
    uow: uow_dep,
    type: str = Form(),
    photo: UploadFile = File()
):
    payment_data = CreatePaymentMethodSchema(
        type=type,
        filename=photo,
    )
    return await payment_methods_service.create_payment_method(uow, payment_data)

@router.get('', response_model=Page[PaymentMethodSchema])
async def get_payment_methods(uow: uow_dep,):
    return await payment_methods_service.get_payment_methods(uow)

@router.get('/{id}',response_model=PaymentMethodSchema)
async def get_payment_method_by_id(
    id: int,
    uow: uow_dep,
):
    return await payment_methods_service.get_payment_method_by_id(uow, id)

@router.put('/{id}',response_model=IdResponseSchema)
async def update_payment_method(
    uow: uow_dep,
    id: int, 
    type: str = Form(),
    photo: UploadFile = File(None)
):
    payment_data = UpdatePaymentMethodSchema(
        type=type,
        filename=photo
    )
    return await payment_methods_service.update_payment_method(uow, id, payment_data)

@router.delete('/{id}',response_model=IdResponseSchema)
async def delete_payment_method(
    id: int,
    uow: uow_dep,
):
    return await payment_methods_service.delete_payment_method(uow, id)
