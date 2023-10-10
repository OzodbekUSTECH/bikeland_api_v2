from fastapi import APIRouter
from services import forms_service
from repositories import Page
from schemas.forms import (
    CreateBackCallWidgetSchema,
    CreateBackCallFormSchema,
    CreateWorkWithUsFormSchema,

    BackCallWidgetSchema,
    BackCallFormSchema,
    WorkWithUsFormSchema
)
from schemas import IdResponseSchema

router = APIRouter(
    prefix="/forms",
    tags=["Forms (BackCallWidget, BackCallForm, WorkWithUsForm)"],
)

@router.post('/bc-widgets', response_model=IdResponseSchema)
async def create_back_call_widget(
    bc_data: CreateBackCallWidgetSchema
):
    return await forms_service.create_bc_widget(bc_data)

@router.post('/bc-forms', response_model=IdResponseSchema)
async def create_back_call_form(
    bc_data: CreateBackCallFormSchema
):
    return await forms_service.create_bc_form(bc_data)

@router.post('/wwu-forms', response_model=IdResponseSchema)
async def create_work_with_us_form(
    wwu_data: CreateWorkWithUsFormSchema
):
    return await forms_service.create_wwu_form(wwu_data)

@router.get('/bc-widgets', response_model=Page[BackCallWidgetSchema])
async def get_back_call_widgets():
    return await forms_service.get_bc_widgets()

@router.get('/bc-forms', response_model=Page[BackCallFormSchema])
async def get_back_call_forms():
    return await forms_service.get_bc_forms()

@router.get('/wwu-forms', response_model=Page[WorkWithUsFormSchema])
async def get_work_with_us_forms():
    return await forms_service.get_wwu_forms()

@router.delete('/bc-widgets/{id}', response_model=IdResponseSchema)
async def delete_back_call_widget(id: int):
    return await forms_service.delete_bc_widget(id)

@router.delete('/bc-forms/{id}',response_model=IdResponseSchema)
async def delete_back_call_form(id: int):
    return await forms_service.delete_bc_form(id)

@router.delete('/wwu-forms/{id}', response_model=IdResponseSchema)
async def delete_work_with_us_form(id: int):
    return await forms_service.delete_wwu_form(id)
