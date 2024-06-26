from schemas.resource_catalog.logos import CreateLogoSchema, UpdateLogoSchema
import models
from database import uow
from utils.media_handler import MediaHandler

class LogosService:

    async def create_logo(self,uow, logo_data: CreateLogoSchema):
        filename = await MediaHandler.save_media(logo_data.filename, MediaHandler.logos_media_dir)
        logo_dict = logo_data.model_dump()
        logo_dict["filename"] = filename
        async with uow:
            logo = await uow.logos.create(logo_dict)
            await uow.commit()
            return logo
        
    
    async def get_logos(self, uow,) -> list[models.Logo]:
        async with uow:
            return await uow.logos.get_all()
        
    async def get_logo_by_id(self,uow, id: int) -> models.Logo:
        async with uow:
            return await uow.logos.get_by_id(id)
        
    async def update_logo(self,uow, id: int, logo_data: UpdateLogoSchema) -> models.Logo:
        filename = await MediaHandler.save_media(logo_data.filename, MediaHandler.logos_media_dir)
        logo_dict = logo_data.model_dump()
        logo_dict["filename"] = filename
        async with uow:
            logo: models.Logo = await uow.logos.get_by_id(id)
            await uow.logos.update(logo.id, logo_dict)
            await uow.commit()
            return logo        

    async def delete_logo(self,uow, id: int) -> models.Logo:
        async with uow:
            logo: models.Logo = await uow.logos.get_by_id(id)
            await uow.logos.delete(logo.id)
            await uow.commit()
            return logo        


logos_service = LogosService()