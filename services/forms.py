from schemas.forms import (
    CreateBackCallWidgetSchema,
    CreateBackCallFormSchema,
    CreateWorkWithUsFormSchema,

    UpdateBackCallWidgetSchema,
    UpdateBackCallFormSchema,
    UpdateWorkWithUsFormSchema
)
import models
from database import uow

class FormsService:

    async def create_bc_widget(self, bc_data: CreateBackCallWidgetSchema) -> models.BackCallWidget:
        async with uow:
            bc_widget = await uow.back_call_widgets.create(bc_data.model_dump())
            await uow.commit()
            return bc_widget
        
    async def create_bc_form(self, bc_data: CreateBackCallFormSchema) -> models.BackCallForm:
        async with uow:
            bc_form = await uow.back_call_forms.create(bc_data.model_dump())
            await uow.commit()
            return bc_form
        
    async def create_wwu_form(self, wwu_data: CreateWorkWithUsFormSchema) -> models.WorkWithUsForm:
        async with uow:
            wwu_form = await uow.work_with_us_forms.create(wwu_data.model_dump())
            await uow.commit()
            return wwu_form
        
    async def get_bc_widgets(self):
        async with uow:
            return await uow.back_call_widgets.get_all()
        
    async def get_bc_forms(self):
        async with uow:
            return await uow.back_call_forms.get_all()
        
    async def get_wwu_forms(self):
        async with uow:
            return await uow.work_with_us_forms.get_all()
        
    #update method dont think, that they should be

    async def delete_bc_widget(self, id: int) -> models.BackCallWidget:
        async with uow:
            bc_widget: models.BackCallWidget = await uow.back_call_widgets.get_by_id(id)
            await uow.back_call_widgets.delete(bc_widget.id)
            await uow.commit()
            return bc_widget
        
    async def delete_bc_form(self, id: int) -> models.BackCallForm:
        async with uow:
            bc_form: models.BackCallForm = await uow.back_call_forms.get_by_id(id)
            await uow.back_call_forms.delete(bc_form.id)
            await uow.commit()
            return bc_form
        
    async def delete_wwu_form(self, id: int) -> models.WorkWithUsForm:
        async with uow:
            wwu_form: models.WorkWithUsForm = await uow.work_with_us_forms.get_by_id(id)
            await uow.work_with_us_forms.delete(wwu_form.id)
            await uow.commit()
            return wwu_form
        
forms_service = FormsService()
