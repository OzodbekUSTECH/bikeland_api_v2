from fastapi import APIRouter, Form, UploadFile, File
from services import dealers_service
from repositories import Page
from schemas.dealers import (
    CreateDealerSchema,
    UpdateDealerSchema,
    DealerSchema,
)
from schemas import IdResponseSchema

router = APIRouter(
    prefix="/dealers",
    tags=["Dealers"],
)

from database import uow_dep
@router.post('', response_model=IdResponseSchema)
async def create_dealer(
    uow: uow_dep,
    full_name: str = Form(),
    photo: UploadFile = File(None),
    phone_number: str = Form()
):
    dealer_data = CreateDealerSchema(
        full_name=full_name,
        filename=photo,
        phone_number=phone_number
    )
    return await dealers_service.create_dealer(uow, dealer_data)

@router.get('', response_model=Page[DealerSchema])
async def get_dealers(uow: uow_dep,):
    return await dealers_service.get_dealers(uow)

@router.get('/{id}', response_model=DealerSchema)
async def get_dealer_by_id(
    id: int,
    uow: uow_dep,
):
    return await dealers_service.get_dealer_by_id(uow, id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_dealer(
    id: int,
    uow: uow_dep,
    full_name: str = Form(),
    photo: UploadFile = File(None),
    phone_number: str = Form()
):
    dealer_data = UpdateDealerSchema(
        full_name=full_name,
        filename=photo,
        phone_number=phone_number
    )
    return await dealers_service.update_dealer(uow, id, dealer_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_dealer(
    id: int,
    uow: uow_dep,
):
    return await dealers_service.delete_dealer(uow, id)