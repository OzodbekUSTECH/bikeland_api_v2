from repositories import BaseRepository
from utils.filters.filter_products import FilterProductsParams
from sqlalchemy import select
from repositories import BaseRepository
from utils.filters.filter_products import FilterProductsParams, ProductFilters
from sqlalchemy import select, and_, func
from fuzzywuzzy import fuzz


class ProductsRepository(BaseRepository):
    async def filter_products(self, params: FilterProductsParams, prod_filter: ProductFilters):
        query = select(self.model)

        # Build the filter conditions based on the parameters in FilterProductsParams
        # filters = []
       
        if params.in_stock is not None:
            if params.in_stock:
                query = query.filter(self.model.quantity > 0)
        #         filters.append(self.model.quantity > 0)
            else:
                query = query.filter(self.model.quantity < 0)


        # if filters:
        #     query = query.where(and_(*filters))

        # Sort the results based on the sorting parameters
        if params.price_by_asc is not None:
            query = query.order_by(self.model.uzb_price.asc() if params.price_by_asc else self.model.uzb_price.desc())

        elif params.by_popularity:
            query = query.order_by(self.model.amount_views.desc())

        elif params.by_new_products:
            query = query.order_by(self.model.id.desc())

        query = prod_filter.filter(query)
        # Execute the query and return the results
        result = await self.session.execute(query)
        return result.scalars().all()
    

    async def get_filtered_products(
            self,
            prod_filter: ProductFilters
    ):
        stmt = select(self.model)
        stmt = prod_filter.filter(stmt)
        result = await self.session.execute(stmt)
        return result.scalars().all()


class ProductMediaGroupsRepository(BaseRepository):
    ...