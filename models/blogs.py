from models import BaseTable
from sqlalchemy import ForeignKey, Text, desc
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from config import settings
    
class BlogMediaGroup(BaseTable):
    __tablename__ = "blog_media_groups"

    blog_id: Mapped[int] = mapped_column(ForeignKey("blogs.id", ondelete='CASCADE'))
    filename: Mapped[str]
    
    @hybrid_property
    def photo_url(self):
        return f"{settings.BLOG_MEDIA_URL}{self.filename}"

class Blog(BaseTable):
    __tablename__ = 'blogs'
    
    title: Mapped[str]
    meta_description: Mapped[str | None]
    description: Mapped[str] = mapped_column(Text)

    photos: Mapped[list["BlogMediaGroup"]] = relationship(cascade="all, delete-orphan", lazy="selectin", order_by=desc("id"))
