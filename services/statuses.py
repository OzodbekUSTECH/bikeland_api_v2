from schemas.statuses import CreateStatusSchema,UpdateStatusSchema
import models

class StatusesService:
    
    async def create_status(self,uow, status_data: CreateStatusSchema) -> models.Status:
        async with uow:
            status = await uow.statuses.create(status_data.model_dump())
            await uow.commit()
            return status
        
    async def get_statuses(self, uow,) -> list[models.Status]:
        async with uow:
            return await uow.statuses.get_all()
        
    async def get_status_by_id(self, uow,id: int) -> models.Status:
        async with uow:
            return await uow.statuses.get_by_id(id)
        
    async def update_status(self,uow, id: int, status_data: UpdateStatusSchema) -> models.Status:
        async with uow:
            status: models.Status = await uow.statuses.get_by_id(id)
            await uow.statuses.update(status.id, status_data.model_dump())
            await uow.commit()
            return status
        
    async def delete_status(self,uow, id: int) -> models.Status:
        async with uow:
            status: models.Status = await uow.statuses.get_by_id(id)
            await uow.statuses.delete(status.id)
            await uow.commit()
            return status
        
statuses_service = StatusesService()