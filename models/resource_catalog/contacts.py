from models import BaseTable
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.hybrid import hybrid_property
from config import settings
    
class Contact(BaseTable):
    __tablename__ = "contacts"

    type: Mapped[str]
    data: Mapped[str]
    filename: Mapped[str]

    @hybrid_property
    def photo_url(self) -> str:
        return f"{settings.CONTACT_MEDIA_URL}{self.filename}"