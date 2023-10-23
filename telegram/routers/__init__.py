from telegram.routers.welcome import router as welcome_router
from telegram.routers.sender import router as sender_router
from telegram.routers.categories import router as categories_router
from telegram.routers.orders import router as orders_router
from telegram.routers.products import router as products_router
from telegram.routers.basket import router as basket_router
from telegram.routers.waiting_lists import router as waiting_lists_router

all_routers = [
    welcome_router,
    sender_router,
    categories_router,
    orders_router,
    waiting_lists_router,
    basket_router,
    products_router,
]