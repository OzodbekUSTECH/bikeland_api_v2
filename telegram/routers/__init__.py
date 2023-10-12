from telegram.routers.welcome import router as welcome_router
from telegram.routers.sender import router as sender_router
from telegram.routers.categories import router as categories_router
from telegram.routers.orders import router as orders_router
from telegram.routers.products import router as products_router

all_routers = [
    welcome_router,
    sender_router,
    categories_router,
    orders_router,
    products_router,
]