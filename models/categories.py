from models import BaseTable
from sqlalchemy import ForeignKey, Text, desc
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from config import settings
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models import SubCategory
    
class Category(BaseTable):
    __tablename__ = "categories"

    name: Mapped[str]

    sub_categories: Mapped[list["SubCategory"]] = relationship(cascade="all, delete-orphan", lazy="subquery")