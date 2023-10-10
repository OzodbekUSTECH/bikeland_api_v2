from models import BaseTable
from sqlalchemy.orm import Mapped

    
class ShowRoom(BaseTable):
    __tablename__ = "show_rooms"

    city: Mapped[str]
    address: Mapped[str]
    landmark: Mapped[str]
    phone_number: Mapped[str]
    location_url: Mapped[str]
