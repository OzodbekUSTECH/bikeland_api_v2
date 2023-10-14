from schemas.show_rooms import CreateShowRoomSchema, UpdateShowRoomSchema
import models
from database import UnitOfWork

class ShowRoomsService:

    def __init__(self):
        self.uow = UnitOfWork()


    async def create_show_room(self, show_room_data: CreateShowRoomSchema) -> models.ShowRoom:
        async with self.uow:
            show_room = await self.uow.show_rooms.create(show_room_data.model_dump())
            await self.uow.commit()
            return show_room
        
    
    async def get_show_rooms(self) -> list[models.ShowRoom]:
        async with self.uow:
            return await self.uow.show_rooms.get_all()
        
    async def get_show_room_by_id(self, id: int) -> models.ShowRoom:
        async with self.uow:
            return await self.uow.show_rooms.get_by_id(id)
        
    async def update_show_room(self, id: int, show_room_data: UpdateShowRoomSchema) -> models.ShowRoom:
        async with self.uow:
            show_room: models.ShowRoom = await self.uow.show_rooms.get_by_id(id)
            await self.uow.show_rooms.update(show_room.id, show_room_data.model_dump())
            await self.uow.commit()
            return show_room
        
    async def delete_show_room(self, id: int) -> models.ShowRoom:
        async with self.uow:
            show_room: models.ShowRoom = await self.uow.show_rooms.get_by_id(id)
            await self.uow.show_rooms.delete(show_room.id)
            await self.uow.commit()
            return show_room
        
show_rooms_service = ShowRoomsService()