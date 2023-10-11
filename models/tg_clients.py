from models import BaseTable
from sqlalchemy import BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models import Order

class TgClient(BaseTable):
    __tablename__ = 'tgclients'

    telegram_id: Mapped[int | None] = mapped_column(BigInteger)
    full_name: Mapped[str | None]
    username: Mapped[str | None]
    phone_number: Mapped[str]

    orders: Mapped[list["Order"]] = relationship(lazy="subquery")

    