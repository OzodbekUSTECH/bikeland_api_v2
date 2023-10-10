from models import BaseTable
from sqlalchemy import ForeignKey, Text, desc
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from config import settings
    
class SubCategory(BaseTable):
    __tablename__ = "sub_categories"

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    name: Mapped[str]