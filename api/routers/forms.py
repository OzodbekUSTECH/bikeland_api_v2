from fastapi import APIRouter
from services import forms_service
from repositories import Page
from schemas.forms import (
    CreateBackCallWidgetSchema,
    CreateBackCallFormSchema,
    CreateWorkWithUsFormSchema,

    BackCallWidgetSchema,
    BackCallFormSchema,
    WorkWithUsFormSchema,

    CreateLinkGoogleForm,
    UpdateLinkGoogleForm,
    LinkGoogleForm
)
from schemas import IdResponseSchema

router = APIRouter(
    prefix="/forms",
    tags=["Forms (BackCallWidget, BackCallForm, WorkWithUsForm)"],
)
from database import uow_dep
@router.post('/bc-widgets', response_model=IdResponseSchema)
async def create_back_call_widget(
    bc_data: CreateBackCallWidgetSchema,
    uow: uow_dep,
):
    return await forms_service.create_bc_widget(uow, bc_data)

@router.post('/bc-forms', response_model=IdResponseSchema)
async def create_back_call_form(
    bc_data: CreateBackCallFormSchema,
    uow: uow_dep,
):
    return await forms_service.create_bc_form(uow, bc_data)

@router.post('/wwu-forms', response_model=IdResponseSchema)
async def create_work_with_us_form(
    wwu_data: CreateWorkWithUsFormSchema,
    uow: uow_dep,
):
    return await forms_service.create_wwu_form(uow, wwu_data)

######################################LINK TO GOOGLE FORM INSTEAD OF WORK WITH US FORMS

@router.post('/link-google-forms', response_model=IdResponseSchema)
async def create_link_to_google_form(
    uow: uow_dep,
    lgf_data: CreateLinkGoogleForm,
):
    return await forms_service.create_link_google_form(uow, lgf_data)

@router.get('/link-google-forms', response_model=Page[LinkGoogleForm])
async def get_link_to_google_forms(
    uow: uow_dep
):
    return await forms_service.get_link_google_forms(uow)

@router.put('/link-google-forms/{id}', response_model=IdResponseSchema)
async def update_link_to_google_form(
    uow: uow_dep,
    id: int,
    lgf_data: UpdateLinkGoogleForm
):
    return await forms_service.update_link_google_form(uow, id, lgf_data)

@router.delete('/link-google-forms/{id}', response_model=IdResponseSchema)
async def delete_link_to_google_form(
    uow: uow_dep,
    id: int,
):
    return await forms_service.delete_link_google_form(uow, id)

######################################LINK TO GOOGLE FORM INSTEAD OF WORK WITH US FORMS
###########################################################################################

@router.get('/bc-widgets', response_model=Page[BackCallWidgetSchema])
async def get_back_call_widgets(uow: uow_dep,):
    return await forms_service.get_bc_widgets(uow)

@router.get('/bc-forms', response_model=Page[BackCallFormSchema])
async def get_back_call_forms(uow: uow_dep,):
    return await forms_service.get_bc_forms(uow)

@router.get('/wwu-forms', response_model=Page[WorkWithUsFormSchema])
async def get_work_with_us_forms(uow: uow_dep,):
    return await forms_service.get_wwu_forms(uow)

@router.delete('/bc-widgets/{id}', response_model=IdResponseSchema)
async def delete_back_call_widget(uow: uow_dep,id: int):
    return await forms_service.delete_bc_widget(uow, id)

@router.delete('/bc-forms/{id}',response_model=IdResponseSchema)
async def delete_back_call_form(uow: uow_dep, id: int):
    return await forms_service.delete_bc_form(uow, id)

@router.delete('/wwu-forms/{id}', response_model=IdResponseSchema)
async def delete_work_with_us_form(uow: uow_dep,id: int):
    return await forms_service.delete_wwu_form(uow, id)
