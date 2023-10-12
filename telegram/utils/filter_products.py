from telegram.btn_names import SorterBtnNames
import models
from datetime import datetime
class FilterProductsHandler:
    
    @staticmethod
    async def filter_products(sort_by: str, products: list[models.Product]) -> list[models.Product]:
        products = list(filter(lambda item: item.quantity > 0, products))
        if sort_by == SorterBtnNames.PRICE_ASC.name:
            sort_key = lambda product: product.uzb_price
            products = sorted(
                products,
                key=sort_key,
                reverse=False
            )
        elif sort_by == SorterBtnNames.PRICE_DESC.name:
            sort_key = lambda product: product.uzb_price
            products = sorted(
                products,
                key=sort_key,
                reverse=True
            )
        elif sort_by == SorterBtnNames.POPULARITY.name:
            sort_key = lambda product: product.amount_views
            products = sorted(
                products,
                key=sort_key,
                reverse=True
            )
        elif sort_by == SorterBtnNames.NEW_PRODUCTS.name:
            sort_key = lambda product: datetime.strptime(product.created_at, "%d.%m.%Y %H:%M:%S")
            products = sorted(
                products,
                key=sort_key,
                reverse=True
            )        
        
        return products