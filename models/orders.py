from models import BaseTable
from sqlalchemy import ForeignKey
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
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(default=1, server_default="1")

    @hybrid_property
    def price(self) -> int:
        return self.product.uzb_price * self.quantity

    @hybrid_property
    def product_title(self) -> str:
        return self.product.title
    
    @hybrid_property
    def brand_name(self) -> str | None:
        return self.product.brand.name if self.product.brand else None
    
    # telegram_client_id: Mapped[int]

    product: Mapped["Product"] = relationship(lazy="subquery")
    