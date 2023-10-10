from models import BaseTable
from sqlalchemy import ForeignKey, Text, desc
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from config import settings
    
class Brand(BaseTable):
    __tablename__ = "brands"

    name: Mapped[str]