from schemas.sub_categories import CreateSubCategorySchema, UpdateSubCategorySchema
import models
from database import uow

class SubCategoriesService:

    async def create_sub_category(self, uow,sub_category_data: CreateSubCategorySchema) -> models.SubCategory:
        async with uow:
            sub_category = await uow.sub_categories.create(sub_category_data.model_dump())
            await uow.commit()
            return sub_category
        
    async def update_sub_category(self, uow,id: int, sub_category_data: UpdateSubCategorySchema) -> models.SubCategory:
        async with uow:
            sub_category: models.SubCategory = await uow.sub_categories.get_by_id(id)
            await uow.sub_categories.update(sub_category.id, sub_category_data.model_dump())
            await uow.commit()
            return sub_category
        
    async def delete_sub_category(self,uow, id: int) -> models.SubCategory:
        async with uow:
            sub_category: models.SubCategory = await uow.sub_categories.get_by_id(id)
            await uow.sub_categories.delete(sub_category.id)
            await uow.commit()
            return sub_category
        
sub_categories_service = SubCategoriesService()