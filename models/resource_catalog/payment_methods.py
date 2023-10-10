from models import BaseTable
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.hybrid import hybrid_property
from config import settings
    
class PaymentMethod(BaseTable):
    __tablename__ = "payment_methods"

    type: Mapped[str]
    filename: Mapped[str]

    @hybrid_property
    def photo_url(self) -> str:
        return f"{settings.PAYMENT_METHOD_MEDIA_URL}{self.filename}"

