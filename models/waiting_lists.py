from models import BaseTable
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models import (
        Product
    )

class WaitingList(BaseTable):
    __tablename__ = 'waiting_lists'

    dealer_id: Mapped[int] = mapped_column(ForeignKey("dealers.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    @hybrid_property
    def title_of_product(self) -> str:
        return self.product.title
    
    @hybrid_property
    def key_of_product(self) -> str:
        return self.product.key
    
    @hybrid_property
    def quantity(self) -> int:
        return self.product.quantity
    
    @hybrid_property
    def min_quantity(self) -> int:
        return self.product.min_quantity
    
    @hybrid_property
    def required_quantity(self) -> int:
        return self.product.min_quantity - self.product.quantity
    
    product: Mapped["Product"] = relationship(lazy="joined")