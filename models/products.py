from models import BaseTable
from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from typing import TYPE_CHECKING
from config import settings
if TYPE_CHECKING:
    from models import (
        Category,
        SubCategory,
        Status,
        Brand,
        Dealer,
        ProductOption,
        ProductVideoLink,
    )


class ProductMediaGroup(BaseTable):
    __tablename__ = 'product_media_groups'

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    filename: Mapped[str]

    @hybrid_property
    def photo_url(self) -> str:
        return f"{settings.PRODUCT_MEDIA_URL}/{self.filename}"
    
class Product(BaseTable):
    __tablename__ = 'products'

    title: Mapped[str]

    @hybrid_property
    def url(self):
        return self.title.replace(' ', 'b').replace('+', 'b').replace('"', 'b').replace('/', 'b') + '_' + str(self.id)
    
    description: Mapped[str | None]
    quantity: Mapped[int]
    min_quantity: Mapped[int] = mapped_column(default=0, server_default="0")
    key: Mapped[str]
    uzb_price: Mapped[int] = mapped_column(BigInteger)
    usd_price: Mapped[int] = mapped_column(BigInteger)
    is_deleted: Mapped[bool] = mapped_column(default=False, server_default="false")

    video_link: Mapped[str | None]
    tag: Mapped[str | None]

    weight: Mapped[str | None]
    clearance: Mapped[str | None]
    fuel_tank_volume: Mapped[str | None]
    fuel_consumption: Mapped[str | None]
    engine: Mapped[str | None]
    max_power: Mapped[str | None]
    max_speed: Mapped[str | None]
    ignition_system: Mapped[str | None]
    gearbox: Mapped[str | None]
    main_gear: Mapped[str | None]
    front_lighting: Mapped[str | None]
    back_lighting: Mapped[str | None]
    front_brake: Mapped[str | None]
    back_brake: Mapped[str | None]
    front_tires: Mapped[str | None]
    back_tires: Mapped[str | None]
    sizes: Mapped[str | None]

    show_on_main_page: Mapped[bool] = mapped_column(default=False, server_default="false")
    show_on_see_also: Mapped[bool] = mapped_column(default=False, server_default="false")

    amount_views: Mapped[int] = mapped_column(default=0, server_default="0")

    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"))
    dealer_id: Mapped[int | None] = mapped_column(ForeignKey("dealers.id"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    sub_category_id: Mapped[int | None] = mapped_column(ForeignKey("sub_categories.id"))
    brand_id: Mapped[int | None] = mapped_column(ForeignKey("brands.id"))
    


    photos: Mapped[list["ProductMediaGroup"]] = relationship(lazy="selectin",  order_by="desc(ProductMediaGroup.id)", cascade="all, delete-orphan")
    dealer: Mapped["Dealer"] = relationship(lazy="joined")
    status: Mapped["Status"] = relationship(lazy="joined")
    category: Mapped["Category"] = relationship(lazy="joined")
    sub_category: Mapped["SubCategory"] = relationship(lazy="joined")
    brand: Mapped["Brand"] = relationship(lazy="joined")

    options: Mapped[list["ProductOption"]] = relationship(lazy="selectin")
    video_links: Mapped[list["ProductVideoLink"]] = relationship(lazy="selectin")

    async def increase_view(self):
        self.amount_views += 1


    