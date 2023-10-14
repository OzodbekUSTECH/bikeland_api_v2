from schemas.categories import CreateCategorySchema, UpdateCategorySchema
import models
from database import UnitOfWork

class CategoriesService:

    def __init__(self):
        self.uow = UnitOfWork()

    async def create_category(self, category_data: CreateCategorySchema) -> models.Category:
        async with self.uow:
            category = await self.uow.categories.create(category_data.model_dump())
            await self.uow.commit()
            return category
        
    async def get_categories(self) -> list[models.Category]:
        async with self.uow:
            return await self.uow.categories.get_all()
        
    async def get_category_by_id(self, id: int) -> models.Category:
        async with self.uow:
            return await self.uow.categories.get_by_id(id)
        
    async def update_category(self, id: int, category_data: CreateCategorySchema) -> models.Category:
        async with self.uow:
            category: models.Category = await self.uow.categories.get_by_id(id)
            await self.uow.categories.update(category.id, category_data.model_dump())
            await self.uow.commit()
            return category
        
    async def delete_category(self, id: int) -> models.Category:
        async with self.uow:
            category: models.Category = await self.uow.categories.get_by_id(id)
            await self.uow.categories.delete(category.id)
            await self.uow.commit()
            return category
        

categories_service = CategoriesService()
    