from schemas.resource_catalog.social_media import CreateSocialNetworkSchema, UpdateSocialNetworkSchema
import models
from utils.media_handler import MediaHandler

class SocialMediaService:

    async def create_social_network(self,uow, social_network_data: CreateSocialNetworkSchema) -> models.SocialNetwork:
        social_network_dict = social_network_data.model_dump()
        filename = await MediaHandler.save_media(social_network_data.filename, MediaHandler.social_media_media_dir)
        social_network_dict["filename"] = filename
        async with uow:
            social_network = await uow.social_media.create(social_network_dict)
            await uow.commit()
            return social_network
        
    
    async def get_social_media(self, uow,) -> list[models.SocialNetwork]:
        async with uow:
            return await uow.social_media.get_all()
        
    async def get_social_network_by_id(self,uow, id: int) -> models.SocialNetwork:
        async with uow:
            return await uow.social_media.get_by_id(id)
        
    async def update_social_network(self,uow, id: int, social_network_data: UpdateSocialNetworkSchema) -> models.SocialNetwork:
        social_network_dict = social_network_data.model_dump(exclude={"filename"})
        if social_network_data.filename is not None:
            filename = await MediaHandler.save_media(social_network_data.filename, MediaHandler.social_media_media_dir)
            social_network_dict["filename"] = filename
        async with uow:
            social_network: models.SocialNetwork = await uow.social_media.get_by_id(id)
            await uow.social_media.update(social_network.id, social_network_dict)
            await uow.commit()
            return social_network
        
    async def delete_social_network(self,uow, id: int) -> models.SocialNetwork:
        async with uow:
            social_network: models.SocialNetwork = await uow.social_media.get_by_id(id)
            await uow.social_media.delete(social_network.id)
            await uow.commit()
            return social_network

social_media_service = SocialMediaService()