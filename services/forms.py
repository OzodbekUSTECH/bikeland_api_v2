from schemas.forms import (
    CreateBackCallWidgetSchema,
    CreateBackCallFormSchema,
    CreateWorkWithUsFormSchema,

)
import models
from database import uow
from config_bot import send_message_to_tg_admins

class FormsService:

    async def _inform_tg_admins(
            self,
            bc_widget: models.BackCallWidget | None = None,
            bc_form: models.BackCallForm | None = None,
            wwu_form: models.WorkWithUsForm | None = None,
            order: models.Order | None = None
        ) -> None:
        if bc_widget is not None:
            message_text = (
                "Название: Форма виджет звонок\n"
                f"Дата: {bc_widget.created_at}\n"
                f"Номер телефона: {bc_widget.phone_number}\n"
            )
        elif bc_form is not None:
            message_text = (
                "Название: Форма обратный звонок\n"
                f"Дата: {bc_form.created_at}\n"
                f"Имя: {bc_form.full_name}\n"
                f"Номер телефона: {bc_form.phone_number}\n"
                f"Город/Регион: {bc_form.location}\n"
                f"Узнал от/из: {bc_form.known_from}\n"
            )
        elif wwu_form is not None:
            message_text = (
                "Название: Форма работа у нас\n"
                f"Дата: {wwu_form.created_at}\n"
                f"Имя: {wwu_form.full_name}\n"
                f"Номер телефона: {wwu_form.phone_number}\n"
                f"О себе: {wwu_form.about}\n"
                f"Узнал от/из: {wwu_form.known_from}"
            )

        elif order is not None:
            message_text = (
                "Заказ из Bikeland.uz\n"
                f"Дата: {order.created_at}\n"
                f"ID/Номер заказа: {order.id}\n"
                f"Имя: {order.name}\n"
                f"Номер телефона: {order.phone_number}\n"   
                f"Название товара: {order.product.title}\n"
                f"Количество: {order.quantity}\n"
                f"Цена:  {order.price:,}".replace(',', ' ') + " сум\n"
                f"Регион {order.region}\n"   
            )
            product: models.Product = await uow.products.get_by_id(order.product_id)
            if product.sub_category:
                message_text +=(
                    f"Категория: {product.sub_category.name}"
                )
            elif product.category:
                message_text +=(
                    f"Категория: {product.category.name}"
                )

        if message_text:
            await send_message_to_tg_admins(message_text)


    async def create_bc_widget(self, bc_data: CreateBackCallWidgetSchema) -> models.BackCallWidget:
        async with uow:
            bc_widget = await uow.back_call_widgets.create(bc_data.model_dump())
            await uow.commit()
            await self._inform_tg_admins(bc_widget=bc_widget)
            return bc_widget
        
    async def create_bc_form(self, bc_data: CreateBackCallFormSchema) -> models.BackCallForm:
        async with uow:
            bc_form = await uow.back_call_forms.create(bc_data.model_dump())
            await uow.commit()
            await self._inform_tg_admins(bc_form=bc_form)
            return bc_form
        
    async def create_wwu_form(self, wwu_data: CreateWorkWithUsFormSchema) -> models.WorkWithUsForm:
        async with uow:
            wwu_form = await uow.work_with_us_forms.create(wwu_data.model_dump())
            await uow.commit()
            await self._inform_tg_admins(wwu_form=wwu_form)
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
