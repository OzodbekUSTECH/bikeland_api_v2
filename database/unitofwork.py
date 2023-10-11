from typing import Type
from database.db import session_maker
import repositories
import models





class UnitOfWork:
    users: Type[repositories.UsersRepository]
    dealers: Type[repositories.DealersRepository]
    blogs: Type[repositories.BlogsRepository]
    blog_media_group: Type[repositories.BlogMediaGroupsRepository]
    brands: Type[repositories.BrandsRepository]
    categories: Type[repositories.CategoriesRepository]
    sub_categories: Type[repositories.SubCategoriesRepository]
    show_rooms: Type[repositories.ShowRoomsRepository]
    statuses: Type[repositories.StatusesRepository]

    contacts: Type[repositories.ContactsRepository]
    logos: Type[repositories.LogosRepository]
    payment_methods: Type[repositories.PaymentMethodsRepository]
    social_media: Type[repositories.SocialMediaRepository]
    delivery: Type[repositories.DeliveryRepository]
    delivery_media: Type[repositories.DeliveryMediaRepository]

    #forms
    back_call_widgets: Type[repositories.BackCallWidgetsRepository]
    back_call_forms: Type[repositories.BackCallFormsRepository]
    work_with_us_forms: Type[repositories.WorkWithUsFormsRepository]

    products: Type[repositories.ProductsRepository]
    product_media_groups: Type[repositories.ProductMediaGroupsRepository]

    orders: Type[repositories.OrdersRepository]

    tgclients: Type[repositories.TgClientsRepository]

    statistics_of_views: Type[repositories.StatisticsOfViewsRepository]
    statistics_of_orders: Type[repositories.StatisticsOfOrdersRepository]
  
    def __init__(self):
        self.session_factory = session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = repositories.UsersRepository(self.session, model=models.User)
        self.dealers = repositories.DealersRepository(self.session, model=models.Dealer)
        self.blogs = repositories.BlogsRepository(self.session, model=models.Blog)
        self.blog_media_group = repositories.BlogMediaGroupsRepository(self.session, model=models.BlogMediaGroup)
        self.brands = repositories.BrandsRepository(self.session, model=models.Brand)
        self.categories = repositories.CategoriesRepository(self.session, model=models.Category)
        self.sub_categories = repositories.SubCategoriesRepository(self.session, model=models.SubCategory)
        self.show_rooms = repositories.ShowRoomsRepository(self.session, model=models.ShowRoom)
        self.statuses = repositories.StatusesRepository(self.session, model=models.Status)

        self.contacts = repositories.ContactsRepository(self.session, model=models.Contact)
        self.logos = repositories.LogosRepository(self.session, model=models.Logo)
        self.payment_methods = repositories.PaymentMethodsRepository(self.session, model=models.PaymentMethod)
        self.social_media = repositories.SocialMediaRepository(self.session, model=models.SocialNetwork)
        self.delivery = repositories.DeliveryRepository(self.session, model=models.Delivery)
        self.delivery_media = repositories.DeliveryMediaRepository(self.session, model=models.DeliveryMedia)

        #forms
        self.back_call_widgets = repositories.BackCallWidgetsRepository(self.session, model=models.BackCallWidget)
        self.back_call_forms = repositories.BackCallFormsRepository(self.session, model=models.BackCallForm)
        self.work_with_us_forms = repositories.WorkWithUsFormsRepository(self.session, model=models.WorkWithUsForm)

        self.products = repositories.ProductsRepository(self.session, model=models.Product)
        self.product_media_groups = repositories.ProductMediaGroupsRepository(self.session, model=models.ProductMediaGroup)

        self.orders = repositories.OrdersRepository(self.session, model=models.Order)

        self.tgclients = repositories.TgClientsRepository(self.session, model=models.TgClient)

        self.statistics_of_views = repositories.StatisticsOfViewsRepository(self.session, model=models.StatisticOfViews)
        self.statistics_of_orders = repositories.StatisticsOfOrdersRepository(self.session, model=models.StatisticOfOrders)

      
    async def __aexit__(self, *args):
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

uow = UnitOfWork()