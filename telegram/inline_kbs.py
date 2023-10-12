from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import settings
import models
from telegram.utils.pagination import Pagination
from telegram.btn_names import SorterBtnNames
from telegram.call_backs import PaginationProductsCallBackData, ChangeBrandCallBackData
class InlineKeyboardsHandler:

    async def get_pagination_ikbs(
            self,
            total_pages: int,
            product: models.Product,
            category_id: int = None,
            sub_category_id: int = None,
            current_page: int = 1,
            sort_by: str = None,
            brand_name: str = None,
    ):
        pagination = Pagination(
            next_btn_name="➡️",
            next_cb_name="next_product",
            prev_btn_name="⬅️",
            prev_cb_name="prev_product",
            current_page=current_page,
            total_pages=total_pages,
            CallBackDataModel=PaginationProductsCallBackData,
            id = product.id,
            category_id=category_id,
            sub_category_id = sub_category_id,
            sort_by = sort_by,
            brand_name = brand_name
        )
        ikbs = await pagination.create_pagination_ikbs()
        sorter_ikbs = await pagination.get_main_sorter_btn()
        row_ikbs = ikbs + sorter_ikbs
        
        
        ikb_markup = InlineKeyboardMarkup(inline_keyboard=row_ikbs)
        return ikb_markup
    

    async def get_brands_ikbs(
            self, 
            products: list[models.Product],
            category_id: int = None,
            sub_category_id: int = None,
            sort_by: str = None,
        ):
        brands_name = ["Все"]
        for product in products:
            if product.brand and product.brand.name not in brands_name:
                brands_name.append(product.brand.name)
        
        ikbs = [
            [InlineKeyboardButton(
                text= brand_name,
                callback_data=PaginationProductsCallBackData(
                    category_id=category_id,
                    sub_category_id=sub_category_id,
                    sort_by = sort_by,
                    brand_name=brand_name,
                ).pack()
            )] for brand_name in brands_name
        ]

        ikb_markup = InlineKeyboardMarkup(
            inline_keyboard=ikbs
        )
        return ikb_markup
    

    async def get_sorter_ikbs(
            self,
            category_id: int = None,
            sub_category_id: int = None,
            sort_by: str = None,
            brand_name: str = None,
        ):
        ikbs = [
            [InlineKeyboardButton(
                text=f"{'✅' if btn.name == sort_by else ''}{btn.value}",
                callback_data=PaginationProductsCallBackData(
                    name= "sorter",
                    # current_page = self.current_page,
                    sort_by = btn.name,
                    category_id = category_id,
                    sub_category_id = sub_category_id,
                    brand_name = brand_name,
                ).pack()
            )] for btn in SorterBtnNames
        ]
        
        ikb = [
            [InlineKeyboardButton(
                text=f"По бренду - {brand_name}",
                callback_data=ChangeBrandCallBackData(
                    category_id = category_id,
                    sub_category_id=sub_category_id,
                    sort_by = sort_by
                ).pack()
            )]
        ]
        row = ikbs + ikb
        ikb_markup = InlineKeyboardMarkup(inline_keyboard=row)
        


        
        return ikb_markup
    

ikbs_handler = InlineKeyboardsHandler()