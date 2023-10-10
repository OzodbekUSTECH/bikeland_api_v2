from models import BaseTable
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.hybrid import hybrid_property
from config import settings
    
class Delivery(BaseTable):
    __tablename__ = "delivery"

    title: Mapped[str]
    description: Mapped[str]

class DeliveryMedia(BaseTable):
    __tablename__ = "delivery_media"

    filename: Mapped[str]

    @hybrid_property
    def photo_url(self) -> str:
        return f"{settings.DELIVERY_MEDIA_URL}{self.filename}"