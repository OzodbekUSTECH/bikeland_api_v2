from schemas.show_rooms import CreateShowRoomSchema, UpdateShowRoomSchema
import models
from database import uow

class ShowRoomsService:

    async def create_show_room(self, show_room_data: CreateShowRoomSchema) -> models.ShowRoom:
        async with uow:
            show_room = await uow.show_rooms.create(show_room_data.model_dump())
            await uow.commit()
            return show_room
        
    
    async def get_show_rooms(self) -> list[models.ShowRoom]:
        async with uow:
            return await uow.show_rooms.get_all()
        
    async def get_show_room_by_id(self, id: int) -> models.ShowRoom:
        async with uow:
            return await uow.show_rooms.get_by_id(id)
        
    async def update_show_room(self, id: int, show_room_data: UpdateShowRoomSchema) -> models.ShowRoom:
        async with uow:
            show_room: models.ShowRoom = await uow.show_rooms.get_by_id(id)
            await uow.show_rooms.update(show_room.id, show_room_data.model_dump())
            await uow.commit()
            return show_room
        
    async def delete_show_room(self, id: int) -> models.ShowRoom:
        async with uow:
            show_room: models.ShowRoom = await uow.show_rooms.get_by_id(id)
            await uow.show_rooms.delete(show_room.id)
            await uow.commit()
            return show_room
        
show_rooms_service = ShowRoomsService()