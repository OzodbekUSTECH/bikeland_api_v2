from aiogram.filters.callback_data import CallbackData
from typing import Optional


class OrderCallBackData(CallbackData, prefix="order"):
    name: str
    product_id: int


class ChangeBrandCallBackData(CallbackData, prefix="categories_callback"):
    category_id: Optional[int] = None
    sub_category_id: Optional[int] = None
    sort_by: Optional[str] = None

class SorterCallBackData(CallbackData, prefix="sorter_cb"):
    category_id: Optional[int] = None
    sub_category_id: Optional[int] = None
    sort_by: Optional[str] = None
    brand_name: Optional[str] = None


class PaginationProductsCallBackData(CallbackData, prefix="prod_cb"):
    name: Optional[str] = None
    current_page: int = 1
    category_id: Optional[int] = None
    sub_category_id: Optional[int] = None
    sort_by: Optional[str] = None
    brand_name: Optional[str] = None


class ChangeBrandCallBackData(CallbackData, prefix="categories_callback"):
    category_id: Optional[int] = None
    sub_category_id: Optional[int] = None
    sort_by: Optional[str] = None




