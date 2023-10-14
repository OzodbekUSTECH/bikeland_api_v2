from fastapi import APIRouter, Depends, UploadFile, File, Form
from services import social_media_service
from repositories import Page
from schemas.resource_catalog.social_media import (
    CreateSocialNetworkSchema,
    UpdateSocialNetworkSchema,
    SocialNetworkSchema,
)
from schemas import IdResponseSchema

router = APIRouter(
    prefix="/social-media",
    tags=["Social Media (resource catalog)"],
)

from database import uow_dep

@router.post('', response_model=IdResponseSchema)
async def create_social_network(
    uow: uow_dep,
    type: str = Form(),
    link: str = Form(),
    photo: UploadFile = File(),
):
    social_network_data = CreateSocialNetworkSchema(
        type=type,
        link=link,
        filename=photo
    )
    return await social_media_service.create_social_network(uow, social_network_data)

@router.get('', response_model=Page[SocialNetworkSchema])
async def get_social_media(uow: uow_dep,):
    return await social_media_service.get_social_media(uow)

@router.get('/{id}', response_model=SocialNetworkSchema)
async def get_social_network_by_id(
    id: int,
    uow: uow_dep,
):
    return await social_media_service.get_social_network_by_id(uow, id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_social_network(
    id: int,
    uow: uow_dep,
    type: str = Form(),
    link: str = Form(),
    photo: UploadFile = File(None),
):
    social_network_data = UpdateSocialNetworkSchema(
        type=type,
        link=link,
        filename=photo
    )
    return await social_media_service.update_social_network(uow, id,social_network_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_social_network(
    id: int,
    uow: uow_dep,
):
    return await social_media_service.delete_social_network(uow, id)