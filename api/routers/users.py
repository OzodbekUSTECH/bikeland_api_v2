from fastapi import APIRouter, Form, UploadFile, File
from services import users_service
from repositories import Page
from schemas.users import (
    CreateUserSchema,
    UpdateUserSchema,
    UserSchema,
)
from schemas import IdResponseSchema
from pydantic import EmailStr

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

from database import uow_dep

@router.post("/{locale}", response_model=IdResponseSchema)
async def create_user(
    uow: uow_dep,
    photo: UploadFile = File(None),
    full_name: str = Form(),
    email: str = Form(),
    phone_number: str = Form(),
    password: str = Form(),
):
    user_data = CreateUserSchema(
        full_name=full_name,
        filename=photo,
        email=email,
        phone_number=phone_number,
        password=password
    )
    return await users_service.create_user(uow,user_data)

@router.get('', response_model=Page[UserSchema])
async def get_users(uow: uow_dep,):
    return await users_service.get_list_of_users(uow)

@router.get('/{id}', response_model=UserSchema)
async def get_user_by_id(
    id: int,
    uow: uow_dep,
):
    return await users_service.get_user_by_id(uow, id)

@router.put('/{id}', response_model=IdResponseSchema)
async def update_user(
    id: int,
    uow: uow_dep,
    photo: UploadFile = File(None),
    full_name: str = Form(),
    email: EmailStr = Form(),
    phone_number: str = Form(),
):
    user_data = UpdateUserSchema(
        full_name=full_name,
        filename=photo,
        email=email,
        phone_number=phone_number,
    )
    return await users_service.update_user(uow, id, user_data)

@router.delete('/{id}', response_model=IdResponseSchema)
async def delete_user(
    id: int,
    uow: uow_dep,
):
    return await users_service.delete_user(uow, id)