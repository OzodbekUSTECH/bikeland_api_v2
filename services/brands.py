from schemas.brands import CreateBrandSchema, UpdateBrandSchema
import models
from database import UnitOfWork

class BrandsService:
    

    def __init__(self):
        self.uow = UnitOfWork()

    async def create_brand(self, brand_data: CreateBrandSchema) -> models.Brand:
        async with self.uow:
            brand = await self.uow.brands.create(brand_data.model_dump())
            await self.uow.commit()
            return brand
        
    async def get_brands(self) -> list[models.Brand]:
        async with self.uow:
            return await self.uow.brands.get_all()
        
    async def get_brand_by_id(self, id: int) -> models.Brand:
        async with self.uow:
            return await self.uow.brands.get_by_id(id)
        
    async def update_brand(self, id: int, brand_data: UpdateBrandSchema) -> models.Brand:
        async with self.uow:
            brand: models.Brand = await self.uow.brands.get_by_id(id)
            await self.uow.brands.update(brand.id, brand_data.model_dump())
            await self.uow.commit()
            return brand
        
    async def delete_brand(self, id: int) -> models.Brand:
        async with self.uow:
            brand: models.Brand = await self.uow.brands.get_by_id(id)
            await self.uow.brands.delete(brand.id)
            await self.uow.commit()
            return brand
        
brands_service = BrandsService()