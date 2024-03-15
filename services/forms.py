from schemas.forms import (
    CreateBackCallWidgetSchema,
    CreateBackCallFormSchema,
    CreateWorkWithUsFormSchema,

    CreateLinkGoogleForm,
    UpdateLinkGoogleForm

)
import models
from config_bot import send_message_to_tg_admins
from database import UnitOfWork

class FormsService:

    async def _inform_tg_admins(
            self,
            uow,
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
            product_data = ""
            
            for basket in order.basket:
                type_of_product = f"- Тип техники: {basket.type_of_product}\n" if basket.type_of_product else ""
                options_data = "Опции: \n" if basket.options else ""
                if basket.options:
                    for option in basket.options:
                        options_data += (
                            f"- Название: {option.name}\n"
                            f"- Цена: {option.price:,}".replace(',', ' ') + " сум\n"  
                        )

                product_data += (
                    f"- Название товара: {basket.title_of_product}\n"
                    f"- Артикул: {basket.key_of_product}\n"
                    f"{type_of_product}"
                    f"- Количество: {basket.quantity}\n"
                    f"- Цена: {basket.price:,}".replace(',', ' ') + " сум\n"
                    f"{options_data}"
                    f"\n"
                )

            message_text = (
                "Заказ из Bikeland.uz\n"
                f"Дата: {order.created_at}\n"
                f"ID/Номер заказа: {order.id}\n"
                f"Имя: {order.name}\n"
                f"Номер телефона: {order.phone_number}\n"  
                f"Регион: {order.region}\n" 
                f"Заказы: \n"  
                f"{product_data}"
                # f"Название товара: {order.basket.title_of_product}\n"
                # f"Количество: {order.quantity}\n"
                f"Цена всего:  {order.total_price:,}".replace(',', ' ') + " сум"
            )
            
            
        if message_text:
            await send_message_to_tg_admins(message_text)


    async def create_bc_widget(self,uow, bc_data: CreateBackCallWidgetSchema) -> models.BackCallWidget:
        async with uow:
            bc_widget = await uow.back_call_widgets.create(bc_data.model_dump())
            await uow.commit()
            await self._inform_tg_admins(uow, bc_widget=bc_widget)
            return bc_widget
        
    async def create_bc_form(self,uow, bc_data: CreateBackCallFormSchema) -> models.BackCallForm:
        async with uow:
            bc_form = await uow.back_call_forms.create(bc_data.model_dump())
            await uow.commit()
            await self._inform_tg_admins(uow, bc_form=bc_form)
            return bc_form
        
    async def create_wwu_form(self,uow, wwu_data: CreateWorkWithUsFormSchema) -> models.WorkWithUsForm:
        async with uow:
            wwu_form = await uow.work_with_us_forms.create(wwu_data.model_dump())
            await uow.commit()
            await self._inform_tg_admins(uow, wwu_form=wwu_form)
            return wwu_form
        
    
    async def create_link_google_form(
            self,
            uow: UnitOfWork,
            lgf_data: CreateLinkGoogleForm
    ) -> models.LinkGoogleForm:
        async with uow:
            link_google_form = await uow.link_google_forms.create(lgf_data.model_dump())
            await uow.commit()
            return link_google_form
        
    async def get_link_google_forms(
            self,
            uow: UnitOfWork
    ) -> list[models.LinkGoogleForm]:
        async with uow:
            return await uow.link_google_forms.get_all()
        
    async def get_one_link_google_form(
            self,
            uow: UnitOfWork
    ) -> models.LinkGoogleForm:
        async with uow:
            return await uow.link_google_forms.get_all_by()
        
    async def update_link_google_form(
            self,
            uow: UnitOfWork,
            id: int,
            lgf_data: UpdateLinkGoogleForm
    ) -> models.LinkGoogleForm:
        async with uow:
            link_google_form: models.LinkGoogleForm = await uow.link_google_forms.update(id, lgf_data.model_dump())
            await uow.commit()
            return link_google_form
        
    async def delete_link_google_form(
            self,
            uow: UnitOfWork,
            id: int
    ) -> models.LinkGoogleForm:
        link_google_form: models.LinkGoogleForm = await uow.link_google_forms.delete(id)
        await uow.commit()
        return link_google_form
                
    async def get_bc_widgets(self,  uow,):
        async with uow:
            return await uow.back_call_widgets.get_all()
        
    async def get_bc_forms(self, uow,):
        async with uow:
            return await uow.back_call_forms.get_all()
        
    async def get_wwu_forms(self, uow,):
        async with uow:
            return await uow.work_with_us_forms.get_all()
        
    #update method dont think, that they should be

    async def delete_bc_widget(self,uow, id: int) -> models.BackCallWidget:
        async with uow:
            bc_widget: models.BackCallWidget = await uow.back_call_widgets.get_by_id(id)
            await uow.back_call_widgets.delete(bc_widget.id)
            await uow.commit()
            return bc_widget
        
    async def delete_bc_form(self,uow, id: int) -> models.BackCallForm:
        async with uow:
            bc_form: models.BackCallForm = await uow.back_call_forms.get_by_id(id)
            await uow.back_call_forms.delete(bc_form.id)
            await uow.commit()
            return bc_form
        
    async def delete_wwu_form(self,uow, id: int) -> models.WorkWithUsForm:
        async with uow:
            wwu_form: models.WorkWithUsForm = await uow.work_with_us_forms.get_by_id(id)
            await uow.work_with_us_forms.delete(wwu_form.id)
            await uow.commit()
            return wwu_form
        
forms_service = FormsService()
