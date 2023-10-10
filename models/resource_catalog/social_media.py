from models import BaseTable
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.hybrid import hybrid_property
from config import settings
    
class SocialNetwork(BaseTable):
    __tablename__ = "social_media"

    type: Mapped[str]
    link: Mapped[str]
    filename: Mapped[str]

    @hybrid_property
    def photo_url(self) -> str:
        return f"{settings.SOCIAL_MEDIA_MEDIA_URL}{self.filename}"