from models import BaseTable
from sqlalchemy.orm import Mapped, mapped_column

class StatisticsTable(BaseTable):
    __abstract__ = True 

    date: Mapped[str]
    quantity: Mapped[int] = mapped_column(default=0, server_default="0")

    async def increase_counter(self) -> None:
        self.quantity += 1


class StatisticOfViews(StatisticsTable):
    __tablename__ = 'statistics_of_views'
    
    


class StatisticOfOrders(StatisticsTable):
    __tablename__ = 'statistics_of_orders'

    
