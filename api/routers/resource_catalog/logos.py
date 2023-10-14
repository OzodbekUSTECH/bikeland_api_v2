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

from database import uow_dep

@router.post('', response_model=IdResponseSchema)
async def create_logo(
    uow: uow_dep,
    photo: UploadFile = File()
):
    logo_data = CreateLogoSchema(
        filename=photo
    )
    return await logos_service.create_logo(uow, logo_data)

@router.get('', response_model=Page[LogoSchema])
async def get_logos(uow: uow_dep,):
    return await logos_service.get_logos(uow)

@router.get('/{id}', response_model=LogoSchema)
async def get_logo_by_id(
    id: int,
    uow: uow_dep,
):
    return await logos_service.get_logo_by_id(uow, id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_logo(
    uow: uow_dep,
    id: int,
    photo: UploadFile = File()
):
    logo_data = UpdateLogoSchema(
        filename=photo
    )
    return await logos_service.update_logo(uow, id, logo_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_logo(
    id: int,
    uow: uow_dep,
):
    return await logos_service.delete_logo(uow, id)

