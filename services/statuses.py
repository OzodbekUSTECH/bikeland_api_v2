from schemas.statuses import CreateStatusSchema,UpdateStatusSchema
import models
from database import UnitOfWork

class StatusesService:
    
    def __init__(self):
        self.uow = UnitOfWork()


    async def create_status(self, status_data: CreateStatusSchema) -> models.Status:
        async with self.uow:
            status = await self.uow.statuses.create(status_data.model_dump())
            await self.uow.commit()
            return status
        
    async def get_statuses(self) -> list[models.Status]:
        async with self.uow:
            return await self.uow.statuses.get_all()
        
    async def get_status_by_id(self, id: int) -> models.Status:
        async with self.uow:
            return await self.uow.statuses.get_by_id(id)
        
    async def update_status(self, id: int, status_data: UpdateStatusSchema) -> models.Status:
        async with self.uow:
            status: models.Status = await self.uow.statuses.get_by_id(id)
            await self.uow.statuses.update(status.id, status_data.model_dump())
            await self.uow.commit()
            return status
        
    async def delete_status(self, id: int) -> models.Status:
        async with self.uow:
            status: models.Status = await self.uow.statuses.get_by_id(id)
            await self.uow.statuses.delete(status.id)
            await self.uow.commit()
            return status
        
statuses_service = StatusesService()