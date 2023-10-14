from schemas.resource_catalog.contacts import CreateContactSchema, UpdateContactSchema
import models
from utils.media_handler import MediaHandler

class ContactsService:

    async def create_contact(self, uow, contact_data: CreateContactSchema) -> models.Contact:
        contact_dict = contact_data.model_dump()
        filename = await MediaHandler.save_media(contact_data.filename, MediaHandler.contacts_media_dir)
        contact_dict["filename"] = filename
        async with uow:
            contact = await uow.contacts.create(contact_dict)
            await uow.commit()
            return contact
        
    async def get_contacts(self, uow, ) -> list[models.Contact]:
        async with uow:
            return await uow.contacts.get_all()
        
    async def get_contact_by_id(self,uow,  id: int) -> models.Contact:
        async with uow:
            return await uow.contacts.get_by_id(id)

    async def update_contact(self,uow,  id: int, contact_data: UpdateContactSchema) -> models.Contact:
        contact_dict = contact_data.model_dump(exclude={"filename"})
        if contact_data.filename is not None:
            filename = await MediaHandler.save_media(contact_data.filename, MediaHandler.contacts_media_dir)
            contact_dict["filename"] = filename
        async with uow:
            contact: models.Contact = await uow.contacts.get_by_id(id)
            await uow.contacts.update(contact.id, contact_dict)
            await uow.commit()
            return contact
        

    async def delete_contact(self, uow, id: int) -> models.Contact:
        async with uow:
            contact: models.Contact = await uow.contacts.get_by_id(id)
            await uow.contacts.delete(contact.id)
            await uow.commit()
            return contact
    
contacts_service = ContactsService()