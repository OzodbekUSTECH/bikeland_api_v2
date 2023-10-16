from repositories import BaseRepository
from utils.filters.filter_products import FilterProductsParams
from sqlalchemy import select
from repositories import BaseRepository
from utils.filters.filter_products import FilterProductsParams
from sqlalchemy import select, and_, func
from fuzzywuzzy import fuzz

class ProductsRepository(BaseRepository):
    async def filter_products(self, params: FilterProductsParams):
        query = select(self.model)

        # Build the filter conditions based on the parameters in FilterProductsParams
        filters = []
        if params.key is not None:
            filters.append(self.model.key == params.key)
            
        if params.category_id is not None:
            filters.append(self.model.category_id == params.category_id)

        if params.sub_category_id is not None:
            filters.append(self.model.sub_category_id == params.sub_category_id)

        if params.dealer_id is not None:
            filters.append(self.model.dealer_id == params.dealer_id)

        if params.title is not None:
            filters.append(func.lower(self.model.title).contains(params.title.lower()))

        if params.status_id is not None:
            filters.append(self.model.status_id == params.status_id)

        if params.brand_id is not None:
            filters.append(self.model.brand_id == params.brand_id)

        if params.show_on_main_page is not None:
            filters.append(self.model.show_on_main_page == params.show_on_main_page)

        if params.show_on_see_also is not None:
            filters.append(self.model.show_on_see_also == params.show_on_see_also)

        if params.in_stock is not None:
            if params.in_stock:
                filters.append(self.model.quantity > 0)
            else:
                filters.append(self.model.quantity <= 0)

        if filters:
            query = query.where(and_(*filters))

        # Sort the results based on the sorting parameters
        if params.price_by_asc is not None:
            sort_key = self.model.uzb_price
            query = query.order_by(sort_key.asc() if params.price_by_asc else sort_key.desc())

        elif params.by_popularity:
            sort_key = self.model.amount_views
            query = query.order_by(sort_key.desc())

        elif params.by_new_products:
            sort_key = self.model.id
            query = query.order_by(sort_key.desc())

        # Execute the query and return the results
        result = await self.session.execute(query)
        return result.scalars().all()


class ProductMediaGroupsRepository(BaseRepository):
    ...