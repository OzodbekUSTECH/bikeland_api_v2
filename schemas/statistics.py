from schemas import CreateBaseModel, UpdateBaseModel, IdResponseSchema
from datetime import datetime


class StatisticsBaseModel(CreateBaseModel):
    date: str = datetime.now().strftime("%d.%m.%Y")
    quantity: int = 0

class CreateStatisticOfViewsSchema(StatisticsBaseModel):
    pass

class CreateStatisticOfOrdersSchema(StatisticsBaseModel):
    pass


class StatisticOfViewsSchema(IdResponseSchema, CreateStatisticOfViewsSchema):
    pass

class StatisticOfOrdersSchema(IdResponseSchema, CreateStatisticOfOrdersSchema):
    pass