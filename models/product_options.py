from models import BaseTable
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class ProductOption(BaseTable):
    __tablename__ = "product_options"

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    name: Mapped[str]
    price: Mapped[int]