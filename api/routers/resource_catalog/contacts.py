from fastapi import APIRouter, Depends, UploadFile, File, Form
from services import contacts_service
from repositories import Page
from schemas.resource_catalog.contacts import (
    CreateContactSchema,
    UpdateContactSchema,
    ContactSchema,
)
from schemas import IdResponseSchema

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts (resource catalog)"],
)

@router.post('', response_model=IdResponseSchema)
async def create_contact(
    type: str = Form(),
    data: str = Form(),
    photo: UploadFile = File()
):
    contact_data = CreateContactSchema(
        type=type,
        data=data,
        filename=photo
    )
    return await contacts_service.create_contact(contact_data)

@router.get('', response_model=Page[ContactSchema])
async def get_contacts():
    return await contacts_service.get_contacts()

@router.get('/{id}', response_model=ContactSchema)
async def get_contact_by_id(
    id: int
):
    return await contacts_service.get_contact_by_id(id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_contact(
    id: int,
    type: str = Form(),
    data: str = Form(),
    photo: UploadFile = File(None)
):
    contact_data = UpdateContactSchema(
        type=type,
        data=data,
        filename=photo
    )
    return await contacts_service.update_contact(id, contact_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_contact(
    id: int
):
    return await contacts_service.delete_contact(id)