from models import BaseTable
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.hybrid import hybrid_property
from config import settings
    
class Logo(BaseTable):
    __tablename__ = "logos"

    filename: Mapped[str]

    @hybrid_property
    def photo_url(self) -> str:
        return f"{settings.LOGO_MEDIA_URL}{self.filename}"
