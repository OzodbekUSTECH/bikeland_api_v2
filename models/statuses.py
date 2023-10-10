from models import BaseTable
from sqlalchemy.orm import Mapped

    
class Status(BaseTable):
    __tablename__ = "statuses"

    name: Mapped[str]