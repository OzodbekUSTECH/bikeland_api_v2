from schemas.statistics import CreateStatisticOfViewsSchema, CreateStatisticOfOrdersSchema
import models
from database import UnitOfWork
from datetime import datetime, timedelta
from utils.exceptions import CustomException

class StatisticsService:

    def __init__(self):
        self.uow = UnitOfWork()


    async def increase_statistic(
            self,
            for_views: bool | None,
            for_orders: bool | None
        ) -> None:
        current_date = datetime.now().strftime("%d.%m.%Y")
        async with self.uow:
            if for_views:
                current_date_of_stats: models.StatisticOfViews = await self.uow.statistics_of_views.get_one_by(date=current_date)
                if not current_date_of_stats:
                    current_date_of_stats: models.StatisticOfViews = await self.uow.statistics_of_views.create(CreateStatisticOfViewsSchema().model_dump())
            elif for_orders:
                current_date_of_stats: models.StatisticOfOrders = await self.uow.statistics_of_orders.get_one_by(date=current_date)
                if not current_date_of_stats:
                    current_date_of_stats: models.StatisticOfOrders = await self.uow.statistics_of_orders.create(CreateStatisticOfOrdersSchema().model_dump())
            else:
                raise CustomException.conflict("Chose for views or orders by giving TRUE value")
            await current_date_of_stats.increase_counter()
            await self.uow.commit()

    async def get_statistics_by_period(
            self,
            for_views: bool | None,
            for_orders: bool | None, 
            start_date: str | None, 
            end_date: str | None
        ) -> list[models.StatisticOfViews] | list[models.StatisticOfOrders]:
        async with self.uow:
            if for_views:
                stats = await self.uow.statistics_of_views.get_by_period(start_date, end_date)
            elif for_orders:
                stats = await self.uow.statistics_of_orders.get_by_period(start_date, end_date)
            else:
                raise CustomException.conflict("Chose for views or orders by giving TRUE value")
            
            return stats
        
    async def calculate_percentage_statistics(
        self,
        for_views: bool | None,
        for_orders: bool | None,
    ):
        today = datetime.now().date()
        one_day_ago = today - timedelta(days=1)
        seven_days_ago = today - timedelta(days=7)
        thirty_days_ago = today - timedelta(days=30)

        today_str = today.strftime("%d.%m.%Y")
        one_day_ago_str = one_day_ago.strftime("%d.%m.%Y")
        seven_days_ago_str = seven_days_ago.strftime("%d.%m.%Y")
        thirty_days_ago_str = thirty_days_ago.strftime("%d.%m.%Y")

        async with self.uow:
            if for_orders:
                today_stats = await self.uow.statistics_of_orders.get_one_by(date=today_str)
                one_day_ago_stats = await self.uow.statistics_of_orders.get_one_by(date=one_day_ago_str)
                seven_days_ago_stats = await self.uow.statistics_of_orders.get_one_by(date=seven_days_ago_str)
                thirty_days_ago_stats = await self.uow.statistics_of_orders.get_one_by(date=thirty_days_ago_str)
            elif for_views:
                today_stats = await self.uow.statistics_of_views.get_one_by(date=today_str)
                one_day_ago_stats = await self.uow.statistics_of_views.get_one_by(date=one_day_ago_str)
                seven_days_ago_stats = await self.uow.statistics_of_views.get_one_by(date=seven_days_ago_str)
                thirty_days_ago_stats = await self.uow.statistics_of_views.get_one_by(date=thirty_days_ago_str)
            else:
                raise ValueError("Either 'for_orders' or 'for_views' must be True")

            # Получаем количество просмотров/заказов за каждый период
            today_count = today_stats.quantity if today_stats else 0
            one_day_ago_count = one_day_ago_stats.quantity if one_day_ago_stats else 0
            seven_days_ago_count = seven_days_ago_stats.quantity if seven_days_ago_stats else 0
            thirty_days_ago_count = thirty_days_ago_stats.quantity if thirty_days_ago_stats else 0

            # Вычисляем проценты относительно 30-дневного периода
            percent_1_day = (today_count / max(1, thirty_days_ago_count)) * 100
            percent_7_days = (seven_days_ago_count / max(1, thirty_days_ago_count)) * 100
            percent_30_days = (thirty_days_ago_count / max(1, thirty_days_ago_count)) * 100

            return {
                "1daypercent": round(min(percent_1_day, 100), 2),
                "7dayspercent": round(min(percent_7_days, 100), 2),
                "30dayspercent": round(min(percent_30_days, 100), 2),
            }



statistics_service = StatisticsService()