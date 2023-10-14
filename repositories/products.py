from repositories import BaseRepository
from utils.filters.filter_products import FilterProductsParams
from sqlalchemy import select
class ProductsRepository(BaseRepository):
    async def filter_products(self, params: FilterProductsParams):
        filter_conditions = params.to_filter_dict()
        if params.in_stock is not None:
            if params.in_stock:
                filter_conditions['quantity'] = (self.model.quantity > 0)
            else:
                filter_conditions['quantity'] = (self.model.quantity <= 0)
        
        query = select(self.model).filter_by(**filter_conditions)
        
        result = await self.session.execute(query)
        filtered_products = result.scalars().all()
        
        # Add sorting logic if needed
        # filtered_products = await params.sort_products(filtered_products)
        
        return filtered_products

class ProductMediaGroupsRepository(BaseRepository):
    ...