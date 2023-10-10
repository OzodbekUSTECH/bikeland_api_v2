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

@router.post('', response_model=IdResponseSchema)
async def create_social_network(
    type: str = Form(),
    link: str = Form(),
    photo: UploadFile = File(),
):
    social_network_data = CreateSocialNetworkSchema(
        type=type,
        link=link,
        filename=photo
    )
    return await social_media_service.create_social_network(social_network_data)

@router.get('', response_model=Page[SocialNetworkSchema])
async def get_social_media():
    return await social_media_service.get_social_media()

@router.get('/{id}', response_model=SocialNetworkSchema)
async def get_social_network_by_id(
    id: int
):
    return await social_media_service.get_social_network_by_id(id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_social_network(
    id: int,
    type: str = Form(),
    link: str = Form(),
    photo: UploadFile = File(None),
):
    social_network_data = UpdateSocialNetworkSchema(
        type=type,
        link=link,
        filename=photo
    )
    return await social_media_service.update_social_network(id,social_network_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_social_network(
    id: int
):
    return await social_media_service.delete_social_network(id)