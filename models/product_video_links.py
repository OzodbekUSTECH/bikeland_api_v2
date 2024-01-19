from models import BaseTable
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class ProductVideoLink(BaseTable):
    __tablename__ = "product_video_links"

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    name: Mapped[str]
    link: Mapped[str]