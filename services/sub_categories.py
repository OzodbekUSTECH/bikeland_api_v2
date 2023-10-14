from schemas.sub_categories import CreateSubCategorySchema, UpdateSubCategorySchema
import models
from database import UnitOfWork

class SubCategoriesService:

    def __init__(self):
        self.uow = UnitOfWork()



    async def create_sub_category(self, sub_category_data: CreateSubCategorySchema) -> models.SubCategory:
        async with self.uow:
            sub_category = await self.uow.sub_categories.create(sub_category_data.model_dump())
            await self.uow.commit()
            return sub_category
        
    async def update_sub_category(self, id: int, sub_category_data: UpdateSubCategorySchema) -> models.SubCategory:
        async with self.uow:
            sub_category: models.SubCategory = await self.uow.sub_categories.get_by_id(id)
            await self.uow.sub_categories.update(sub_category.id, sub_category_data.model_dump())
            await self.uow.commit()
            return sub_category
        
    async def delete_sub_category(self, id: int) -> models.SubCategory:
        async with self.uow:
            sub_category: models.SubCategory = await self.uow.sub_categories.get_by_id(id)
            await self.uow.sub_categories.delete(sub_category.id)
            await self.uow.commit()
            return sub_category
        
sub_categories_service = SubCategoriesService()