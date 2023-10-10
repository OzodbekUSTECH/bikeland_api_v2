from fastapi import APIRouter, Depends, UploadFile, File
from services import logos_service
from repositories import Page
from schemas.resource_catalog.logos import (
    CreateLogoSchema,
    UpdateLogoSchema,
    LogoSchema,
)
from schemas import IdResponseSchema

router = APIRouter(
    prefix="/logos",
    tags=["Logos (resource catalog)"],
)

@router.post('', response_model=IdResponseSchema)
async def create_logo(
    photo: UploadFile = File()
):
    logo_data = CreateLogoSchema(
        filename=photo
    )
    return await logos_service.create_logo(logo_data)

@router.get('', response_model=Page[LogoSchema])
async def get_logos():
    return await logos_service.get_logos()

@router.get('/{id}', response_model=LogoSchema)
async def get_logo_by_id(
    id: int
):
    return await logos_service.get_logo_by_id(id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_logo(
    id: int,
    photo: UploadFile = File()
):
    logo_data = UpdateLogoSchema(
        filename=photo
    )
    return await logos_service.update_logo(id, logo_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_logo(
    id: int
):
    return await logos_service.delete_logo(id)

