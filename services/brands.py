from schemas.brands import CreateBrandSchema, UpdateBrandSchema
import models
from database import uow

class BrandsService:
    
    async def create_brand(self, brand_data: CreateBrandSchema) -> models.Brand:
        async with uow:
            brand = await uow.brands.create(brand_data.model_dump())
            await uow.commit()
            return brand
        
    async def get_brands(self) -> list[models.Brand]:
        async with uow:
            return await uow.brands.get_all()
        
    async def get_brand_by_id(self, id: int) -> models.Brand:
        async with uow:
            return await uow.brands.get_by_id(id)
        
    async def update_brand(self, id: int, brand_data: UpdateBrandSchema) -> models.Brand:
        async with uow:
            brand: models.Brand = await uow.brands.get_by_id(id)
            await uow.brands.update(brand.id, brand_data.model_dump())
            await uow.commit()
            return brand
        
    async def delete_brand(self, id: int) -> models.Brand:
        async with uow:
            brand: models.Brand = await uow.brands.get_by_id(id)
            await uow.brands.delete(brand.id)
            await uow.commit()
            return brand
        
brands_service = BrandsService()