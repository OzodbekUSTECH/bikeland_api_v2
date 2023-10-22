from models import BaseTable
from sqlalchemy import ForeignKey, ARRAY, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from typing import TYPE_CHECKING
from config import settings
if TYPE_CHECKING:
    from models import Product
    
class Order(BaseTable):
    __tablename__ = 'orders'
    
    name: Mapped[str]
    phone_number: Mapped[str]
    region: Mapped[str]
    known_from: Mapped[str | None]
    # product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    # quantity: Mapped[int] = mapped_column(default=1, server_default="1")
    source: Mapped[str] = mapped_column(default="Bikeland.uz", server_default="Bikeland.uz")

    @hybrid_property
    def total_price(self) -> int:
        default_price = 0
        for product in self.basket:
            default_price += product.price
        return default_price

    basket: Mapped[list["OrderBasket"]] = relationship(lazy="subquery")
    # @hybrid_property
    # def product_title(self) -> str:
    #     return self.product.title
    
    
    
    
        
    
    # product: Mapped["Product"] = relationship(lazy="immediate")

    

class OrderBasket(BaseTable):
    __tablename__ = "orders_basket"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]
    option_ids: Mapped[str | None]  = mapped_column(ARRAY(Integer))
    
    @hybrid_property
    def options(self) -> list:
        options_data = []
        if self.option_ids:
            for option in self.product.options:
                if option.id in self.option_ids:
                    options_data.append(option)
        return options_data


    @hybrid_property
    def price(self) -> int:
        return self.product.uzb_price * self.quantity
    

    @hybrid_property
    def price_with_options(self) -> int | None:
        if self.options:
            default_price = self.price
            for option in self.options:
                default_price += option.price
            return default_price
        return None
    
    @hybrid_property
    def title_of_product(self) -> str:
        return self.product.title
    
    @hybrid_property
    def key_of_product(self) -> str:
        return self.product.key
    
    @hybrid_property
    def type_of_product(self) -> str | None:
        if self.product.sub_category_id:
            return self.product.sub_category.name
        elif self.product.category_id:
            return self.product.category.name
                
    
    product: Mapped["Product"] = relationship(lazy="subquery")
    order: Mapped["Order"] = relationship(lazy="subquery")

    tgclient_id: Mapped[int] = mapped_column(ForeignKey("tgclients.id"))
    