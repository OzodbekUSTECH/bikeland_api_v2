from typing import Annotated
from fastapi import APIRouter, Depends, Form
from pydantic import EmailStr
from services import users_service
from utils.dependencies import get_current_user
from schemas.users import (
    TokenSchema,
    UserSchema,
    ResetPasswordSchema
)
from schemas import IdResponseSchema
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/login", response_model=TokenSchema)
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return await users_service.authenticate_user(form_data.username, form_data.password)

@router.get("/me", response_model=UserSchema)
async def get_own_user(
    current_user=Depends(get_current_user),
):
    return current_user


