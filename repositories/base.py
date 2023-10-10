from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import desc
from utils.exceptions import CustomException
from typing import Type

class BaseRepository:
    def __init__(self, session: AsyncSession, model: DeclarativeMeta):
        self.session = session
        self.model = model

    async def bulk_create(self, data_list: list[dict]):
        stmt = insert(self.model).values(data_list).returning(self.model)
        await self.session.execute(stmt)

    async def create(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_all(self, reverse: bool = False):
        stmt = select(self.model)
        if reverse:
            stmt = stmt.order_by(desc(self.model.id))
        else:
            stmt = stmt.order_by(self.model.id)
        
        return await paginate(self.session, stmt)

    async def get_by_id(self, id: int) -> dict:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()
        
        if item is None:
            raise CustomException.not_found("id doesnt exist")
        
        return item


    async def get_by_email(self, email: str) -> dict:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, id: int, data: dict) -> dict:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete(self, id: int) -> dict:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)
        try:
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except:
            raise CustomException.forbidden("Нельзя удалить, из-за foreignkeys")


    async def delete_by(self, **filters) -> dict:
        stmt = delete(self.model).filter_by(**filters).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def get_one_by(self, **filters) -> dict:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all_without_pagination(self, reverse: bool = False):
        stmt = select(self.model)
        if reverse:
            stmt.order_by(desc(self.model.id))
        else:
            stmt.order_by(self.model.id)

        result = await self.session.execute(stmt)
        return result.scalars().all()