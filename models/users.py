from models import BaseTable
from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from typing import TYPE_CHECKING
from config import settings
    
class User(BaseTable):
    __tablename__ = 'users'
    
    full_name: Mapped[str]
    filename: Mapped[str | None]
    password: Mapped[str]
    email: Mapped[str]
    phone_number: Mapped[str]

    
    # role_id = Column(Integer, ForeignKey('roles.id'))
    # role = relationship("Role",back_populates="users", lazy="subquery")
    # products = relationship("Product",back_populates="user", lazy="subquery")
    # notifications = relationship("Notification", lazy="subquery")

    # @hybrid_property
    # def amount_notifications(self):
    #     res = [notification for notification in self.notifications if notification.has_seen == False]
    #     return len(res)

    @hybrid_property
    def photo_url(self) -> str | None:
        if self.filename:
            return f"{settings.USER_MEDIA_URL}{self.filename}"
        else:
            return None


