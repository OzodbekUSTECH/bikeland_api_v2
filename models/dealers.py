from models import BaseTable
from sqlalchemy import BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from typing import TYPE_CHECKING
from config import settings
    
class Dealer(BaseTable):
    __tablename__ = 'dealers'
    
    full_name: Mapped[str]
    filename: Mapped[str | None]
    phone_number: Mapped[str]
    telegram_id: Mapped[int | None] = mapped_column(BigInteger)

    @hybrid_property
    def photo_url(self) -> str | None:
        if self.filename:
            return f"{settings.DEALER_MEDIA_URL}{self.filename}"
        else:
            return None