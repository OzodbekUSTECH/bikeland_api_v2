from schemas.resource_catalog.logos import CreateLogoSchema, UpdateLogoSchema
import models
from database import UnitOfWork
from utils.media_handler import MediaHandler

class LogosService:

    def __init__(self):
        self.uow = UnitOfWork()

    async def create_logo(self, logo_data: CreateLogoSchema):
        filename = await MediaHandler.save_media(logo_data.filename, MediaHandler.logos_media_dir)
        logo_dict = logo_data.model_dump()
        logo_dict["filename"] = filename
        async with self.uow:
            logo = await self.uow.logos.create(logo_dict)
            await self.uow.commit()
            return logo
        
    
    async def get_logos(self) -> list[models.Logo]:
        async with self.uow:
            return await self.uow.logos.get_all()
        
    async def get_logo_by_id(self, id: int) -> models.Logo:
        async with self.uow:
            return await self.uow.logos.get_by_id(id)
        
    async def update_logo(self, id: int, logo_data: UpdateLogoSchema) -> models.Logo:
        filename = await MediaHandler.save_media(logo_data.filename, MediaHandler.logos_media_dir)
        logo_dict = logo_data.model_dump()
        logo_dict["filename"] = filename
        async with self.uow:
            logo: models.Logo = await self.uow.logos.get_by_id(id)
            await self.uow.logos.update(logo.id, logo_dict)
            await self.uow.commit()
            return logo        

    async def delete_logo(self, id: int) -> models.Logo:
        async with self.uow:
            logo: models.Logo = await self.uow.logos.get_by_id(id)
            await self.uow.logos.delete(logo.id)
            await self.uow.commit()
            return logo        


logos_service = LogosService()