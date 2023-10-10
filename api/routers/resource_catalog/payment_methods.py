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

@router.post('', response_model=IdResponseSchema)
async def create_payment_method(
    type: str = Form(),
    photo: UploadFile = File()
):
    payment_data = CreatePaymentMethodSchema(
        type=type,
        filename=photo,
    )
    return await payment_methods_service.create_payment_method(payment_data)

@router.get('', response_model=Page[PaymentMethodSchema])
async def get_payment_methods():
    return await payment_methods_service.get_payment_methods()

@router.get('/{id}',response_model=PaymentMethodSchema)
async def get_payment_method_by_id(
    id: int
):
    return await payment_methods_service.get_payment_method_by_id(id)

@router.put('/{id}',response_model=IdResponseSchema)
async def update_payment_method(
    id: int, 
    type: str = Form(),
    photo: UploadFile = File(None)
):
    payment_data = UpdatePaymentMethodSchema(
        type=type,
        filename=photo
    )
    return await payment_methods_service.update_payment_method(id, payment_data)

@router.delete('/{id}',response_model=IdResponseSchema)
async def delete_payment_method(
    id: int
):
    return await payment_methods_service.delete_payment_method(id)
