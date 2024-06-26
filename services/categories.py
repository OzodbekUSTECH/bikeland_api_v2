from schemas.categories import CreateCategorySchema, UpdateCategorySchema
import models

class CategoriesService:

    async def create_category(self,uow, category_data: CreateCategorySchema) -> models.Category:
        async with uow:
            category = await uow.categories.create(category_data.model_dump())
            await uow.commit()
            return category
        
    async def get_categories(self,uow,) -> list[models.Category]:
        async with uow:
            return await uow.categories.get_all()
        
    async def get_category_by_id(self,uow, id: int) -> models.Category:
        async with uow:
            return await uow.categories.get_by_id(id)
        
    async def update_category(self,uow, id: int, category_data: CreateCategorySchema) -> models.Category:
        async with uow:
            category: models.Category = await uow.categories.get_by_id(id)
            await uow.categories.update(category.id, category_data.model_dump())
            await uow.commit()
            return category
        
    async def delete_category(self,uow, id: int) -> models.Category:
        async with uow:
            category: models.Category = await uow.categories.get_by_id(id)
            await uow.categories.delete(category.id)
            await uow.commit()
            return category
        

categories_service = CategoriesService()
    