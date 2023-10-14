from schemas.resource_catalog.contacts import CreateContactSchema, UpdateContactSchema
import models
from database import UnitOfWork
from utils.media_handler import MediaHandler

class ContactsService:

    def __init__(self):
        self.uow = UnitOfWork()

    async def create_contact(self, contact_data: CreateContactSchema) -> models.Contact:
        contact_dict = contact_data.model_dump()
        filename = await MediaHandler.save_media(contact_data.filename, MediaHandler.contacts_media_dir)
        contact_dict["filename"] = filename
        async with self.uow:
            contact = await self.uow.contacts.create(contact_dict)
            await self.uow.commit()
            return contact
        
    async def get_contacts(self) -> list[models.Contact]:
        async with self.uow:
            return await self.uow.contacts.get_all()
        
    async def get_contact_by_id(self, id: int) -> models.Contact:
        async with self.uow:
            return await self.uow.contacts.get_by_id(id)

    async def update_contact(self, id: int, contact_data: UpdateContactSchema) -> models.Contact:
        contact_dict = contact_data.model_dump(exclude={"filename"})
        if contact_data.filename is not None:
            filename = await MediaHandler.save_media(contact_data.filename, MediaHandler.contacts_media_dir)
            contact_dict["filename"] = filename
        async with self.uow:
            contact: models.Contact = await self.uow.contacts.get_by_id(id)
            await self.uow.contacts.update(contact.id, contact_dict)
            await self.uow.commit()
            return contact
        

    async def delete_contact(self, id: int) -> models.Contact:
        async with self.uow:
            contact: models.Contact = await self.uow.contacts.get_by_id(id)
            await self.uow.contacts.delete(contact.id)
            await self.uow.commit()
            return contact
    
contacts_service = ContactsService()