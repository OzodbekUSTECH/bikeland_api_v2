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


@router.post('', response_model=IdResponseSchema)
async def create_dealer(
    full_name: str = Form(),
    photo: UploadFile = File(None),
    phone_number: str = Form()
):
    dealer_data = CreateDealerSchema(
        full_name=full_name,
        filename=photo,
        phone_number=phone_number
    )
    return await dealers_service.create_dealer(dealer_data)

@router.get('', response_model=Page[DealerSchema])
async def get_dealers():
    return await dealers_service.get_dealers()

@router.get('/{id}', response_model=DealerSchema)
async def get_dealer_by_id(
    id: int
):
    return await dealers_service.get_dealer_by_id(id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_dealer(
    id: int,
    full_name: str = Form(),
    photo: UploadFile = File(None),
    phone_number: str = Form()
):
    dealer_data = UpdateDealerSchema(
        full_name=full_name,
        filename=photo,
        phone_number=phone_number
    )
    return await dealers_service.update_dealer(id, dealer_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_dealer(
    id: int
):
    return await dealers_service.delete_dealer(id)