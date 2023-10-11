from fastapi import APIRouter
from services import statistics_service
from repositories import Page
from schemas.statistics import (
    StatisticOfViewsSchema,
    StatisticOfOrdersSchema
)
from schemas import IdResponseSchema

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics of Views and Orders"],
)

@router.post('')
async def increase_statistic(
    for_views: bool = None,
    for_orders: bool= None
) -> None:
    return await statistics_service.increase_statistic(for_views, for_orders)

@router.get('/line-graph', response_model=list[StatisticOfViewsSchema] | list[StatisticOfOrdersSchema])
async def get_statistics_by_period_for_line_graph(
    for_views: bool = None,
    for_orders: bool = None,
    start_date: str | None = None,
    end_date: str | None = None
):
    return await statistics_service.get_statistics_by_period(for_views, for_orders, start_date, end_date)

@router.get('/pie-charts')
async def get_statistics_for_pie_charts(
    for_views: bool = None,
    for_orders: bool = None
):
    return await statistics_service.calculate_percentage_statistics(for_views, for_orders)
    
    