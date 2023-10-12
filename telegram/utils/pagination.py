from aiogram.types import InlineKeyboardButton
from telegram.call_backs import OrderCallBackData
from telegram.btn_names import  SorterBtnNames
from telegram.call_backs import ChangeBrandCallBackData
from telegram.call_backs import SorterCallBackData


class Pagination:
    def __init__(
            self,
            next_btn_name: str,
            next_cb_name: str,
            prev_btn_name: str,
            prev_cb_name: str,
            current_page: int,
            total_pages: int,
            id: int,
            CallBackDataModel,
            **kwargs
    ):
        self.next_btn_name = next_btn_name
        self.next_cb_name = next_cb_name
        self.prev_btn_name = prev_btn_name
        self.prev_cb_name = prev_cb_name
        self.current_page = current_page
        self.total_pages = total_pages
        self.id = id
        self.callbackdatamodel = CallBackDataModel
        self.kwargs = kwargs


    async def get_main_sorter_btn(self):
        ikb = [
            [InlineKeyboardButton(
                text="Сортировка",
                callback_data=SorterCallBackData(
                    category_id = self.kwargs.get('category_id'),
                    sub_category_id=self.kwargs.get('sub_category_id'),
                    sort_by = self.kwargs.get('sort_by'),
                    brand_name = self.kwargs.get('brand_name')
                ).pack()
            )]
        ]

        return ikb

    async def get_sorter_ikbs(
            self,
        ):
        ikbs = [
            [InlineKeyboardButton(
                text=f"{'✅' if btn.name == self.kwargs.get('sort_by') else ''}{btn.value}",
                callback_data=self.callbackdatamodel(
                    name= "sorter",
                    # current_page = self.current_page,
                    sort_by = btn.name,
                    category_id = self.kwargs.get("category_id"),
                    sub_category_id = self.kwargs.get('sub_category_id'),
                    brand_name = self.kwargs.get('brand_name')
                ).pack()
            )] for btn in SorterBtnNames
        ]
        
        ikb = [
            [InlineKeyboardButton(
                text=f"По бренду - {self.kwargs.get('brand_name')}",
                callback_data=ChangeBrandCallBackData(
                    category_id = self.kwargs.get('category_id'),
                    sub_category_id=self.kwargs.get('sub_category_id'),
                    sort_by = self.kwargs.get('sort_by')
                ).pack()
            )]
        ]
        


        
        return ikbs + ikb

    async def create_pagination_ikbs(self):
        
            
        prev_button = InlineKeyboardButton(
            text=self.prev_btn_name,
            callback_data=self.callbackdatamodel(
                name = self.prev_cb_name,
                current_page=self.current_page,
                **self.kwargs
            ).pack()
        )

        page_button = InlineKeyboardButton(text=f"{self.current_page}/{self.total_pages}", callback_data="show_page")

        next_button = InlineKeyboardButton(
            text=self.next_btn_name,
            callback_data=self.callbackdatamodel(
                name = self.next_cb_name,
                current_page=self.current_page,
                **self.kwargs
            ).pack()
        )
        order_btn = InlineKeyboardButton(
            text="Заказать",
            callback_data=OrderCallBackData(
                name="order",
                product_id=self.id,
            ).pack()
        )
        row = [[prev_button, page_button, next_button], [order_btn]]
        return row
    

    async def create_basket_ikbs(self):
        prev_button = InlineKeyboardButton(
            text=self.prev_btn_name,
            callback_data=self.callbackdatamodel(
                name = self.prev_cb_name,
                current_page=self.current_page,
                **self.kwargs
            ).pack()
        )

        page_button = InlineKeyboardButton(text=f"{self.current_page}/{self.total_pages}", callback_data="show_page")

        next_button = InlineKeyboardButton(
            text=self.next_btn_name,
            callback_data=self.callbackdatamodel(
                name = self.next_cb_name,
                current_page=self.current_page,
                **self.kwargs
            ).pack()
        )
        
        
        row = [[prev_button, page_button, next_button]]
        return row

    