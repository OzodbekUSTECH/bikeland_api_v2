from fastapi import Query
from fuzzywuzzy import fuzz
import models
from utils.filters.base import BaseFilterParams


class FilterProductsParams(BaseFilterParams):
    def __init__(
            self,
            category_id: int = Query(None),
            sub_category_id: int = Query(None),
            dealer_id: int = Query(None),
            title: str = Query(None),
            status_id: int = Query(None),
            brand_id: int = Query(None),
            in_stock: bool = Query(None),

            price_by_asc: bool = Query(None),
            by_popularity: bool = Query(None),
            by_new_products: bool = Query(None),  

            show_on_main_page: bool = Query(None),
            show_on_see_also: bool = Query(None),

            with_pagination: bool = Query(False),
    ):
        self.category_id = category_id
        self.sub_category_id = sub_category_id
        self.dealer_id = dealer_id
        self.title = title
        self.status_id = status_id
        self.brand_id = brand_id
        self.in_stock = in_stock

        self.price_by_asc = price_by_asc
        self.by_popularity = by_popularity
        self.by_new_products = by_new_products

        self.show_on_main_page = show_on_main_page
        self.show_on_see_also = show_on_see_also

        self.with_pagination = with_pagination

    def filter_item(self, product: models.Product):
        # Список условий фильтрации
        filters = []

        if self.category_id is not None:
            filters.append(self.category_id == product.category_id)

        if self.sub_category_id is not None:
            filters.append(self.sub_category_id == product.sub_category_id)
        
        if self.dealer_id is not None:
            filters.append(self.dealer_id == product.dealer_id)

        if self.title is not None:
            filters.append(
                fuzz.partial_ratio(
                    self.title.lower(), product.title.lower()
                ) >= 75
            )

        if self.status_id is not None:
            filters.append(self.status_id == product.status_id)

        if self.brand_id is not None:
            filters.append(self.brand_id == product.brand_id)

        if self.show_on_main_page is not None:
            filters.append(self.show_on_main_page == product.show_on_main_page)

        if self.show_on_see_also is not None:
            filters.append(self.show_on_see_also == product.show_on_see_also)

        if self.in_stock is not None:
            if self.in_stock:
                filters.append(product.quantity > 0)
            else:
                filters.append(product.quantity <= 0)

        return all(filters)

    def sort_products(self, products: list[models.Product]) -> list[models.Product]:
        if self.price_by_asc is not None:
            sort_key = lambda product: product.uzb_price
            products = sorted(
                products,
                key=sort_key,
                reverse=not self.price_by_asc
            )
            

        elif self.by_popularity:
            sort_key = lambda product: product.amount_views
            products = sorted(
                products,
                key=sort_key,
                reverse= True
            )
        
        elif self.by_new_products:
            sort_key = lambda product: product.id
            products = sorted(
                products,
                key=sort_key,
                reverse=True
            )
        
        return products


    def to_filter_dict(self):
        filter_dict = {}

        if self.category_id is not None:
            filter_dict['category_id'] = self.category_id

        if self.sub_category_id is not None:
            filter_dict['sub_category_id'] = self.sub_category_id

        if self.dealer_id is not None:
            filter_dict['dealer_id'] = self.dealer_id

        # if self.title is not None:
        #     # Add fuzzy matching if needed
        #     filter_dict['title'] = self.title.lower()

        if self.status_id is not None:
            filter_dict['status_id'] = self.status_id

        if self.brand_id is not None:
            filter_dict['brand_id'] = self.brand_id

        if self.show_on_main_page is not None:
            filter_dict['show_on_main_page'] = self.show_on_main_page

        if self.show_on_see_also is not None:
            filter_dict['show_on_see_also'] = self.show_on_see_also

        

        return filter_dict
    