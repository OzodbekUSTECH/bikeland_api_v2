from fastapi import APIRouter
from services import show_rooms_service
from repositories import Page
from schemas.show_rooms import (
    CreateShowRoomSchema,
    UpdateShowRoomSchema,
    ShowRoomSchema,
)
from schemas import IdResponseSchema

router = APIRouter(
    prefix="/show-rooms",
    tags=["Show Rooms"],
)
from database import uow_dep

@router.post('', response_model=IdResponseSchema)
async def create_show_room(
    uow: uow_dep,
    show_room_data: CreateShowRoomSchema
):
    return await show_rooms_service.create_show_room(uow, show_room_data)

@router.get('', response_model=Page[ShowRoomSchema])
async def get_show_rooms(uow: uow_dep,):
    return await show_rooms_service.get_show_rooms(uow)

@router.get('/{id}', response_model=ShowRoomSchema)
async def get_show_room_by_id(
    id: int,
    uow: uow_dep,
):
    return await show_rooms_service.get_show_room_by_id(uow, id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_show_room(
    id: int,
    uow: uow_dep,
    show_room_data: UpdateShowRoomSchema
):
    return await show_rooms_service.update_show_room(uow, id, show_room_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_show_room(
    id: int,
    uow: uow_dep,
):
    return await show_rooms_service.delete_show_room(uow, id)