from fastapi import APIRouter
from services import statuses_service
from repositories import Page
from schemas.statuses import (
    CreateStatusSchema,
    UpdateStatusSchema,
    StatusSchema,
)
from schemas import IdResponseSchema

router = APIRouter(
    prefix="/statuses",
    tags=["Statuses"],
)

@router.post('', response_model=IdResponseSchema)
async def create_status(
    status_data: CreateStatusSchema
):
    return await statuses_service.create_status(status_data)

@router.get('', response_model=Page[StatusSchema])
async def get_statuses():
    return await statuses_service.get_statuses()

@router.get('/{id}', response_model=StatusSchema)
async def get_status_by_id(
    id: int
):
    return await statuses_service.get_status_by_id(id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_status(
    id: int,
    status_data: UpdateStatusSchema
):
    return await statuses_service.update_status(id, status_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_status(
    id: int
):
    return await statuses_service.delete_status(id)