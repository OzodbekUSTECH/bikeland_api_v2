from api.routers.auth import router as auth_router
from api.routers.users import router as users_router
from api.routers.dealers import router as dealers_router
from api.routers.blogs import router as blogs_router
from api.routers.show_rooms import router as show_rooms_router
from api.routers.brands import router as brands_router
from api.routers.categories import router as categories_router
from api.routers.sub_categories import router as sub_categories_router
from api.routers.statuses import router as statuses_router

from api.routers.resource_catalog.contacts import router as contacts_router
from api.routers.resource_catalog.logos import router as logos_router
from api.routers.resource_catalog.payment_methods import router as payment_methods_router
from api.routers.resource_catalog.social_media import router as social_media_router
from api.routers.resource_catalog.delivery import router as delivery_router

from api.routers.forms import router as forms_router


from api.routers.parser import router as router_parser

all_routers = [
    router_parser,
    auth_router,
    users_router,
    dealers_router,
    blogs_router,
    show_rooms_router,
    brands_router,
    categories_router,
    sub_categories_router,
    statuses_router,

    #resource catalog
    contacts_router,
    logos_router,
    payment_methods_router,
    social_media_router,
    delivery_router,

    forms_router
]