from fastapi import Query
from fuzzywuzzy import fuzz
import models


class BaseFilterParams:
    def __init__(self):
        pass

    async def get_filtered_items(self, items, *args, **kwargs):
        filtered_items = list(filter(lambda item: self.filter_item(item, *args, **kwargs), items))
        return filtered_items

    def filter_item(self, item, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the filter_item method.")

