from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseTable(DeclarativeBase):
    __abstract__ = True 

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    created_at: Mapped[str | None]  
    updated_at: Mapped[str | None]  
    
    
    
    
