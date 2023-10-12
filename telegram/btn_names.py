from enum import Enum

class WelcomeBtnNames(Enum):
    BIKE = "Мототехника 🏍"
    EQUIPS = "Экип и запчасти 🛠"
    BASKET = "Корзина 🛍"
    

class SorterBtnNames(Enum):
    DEFAULT = "По умолчанию"
    PRICE_ASC = "Цена - по возрастанию"
    PRICE_DESC = "Цена - по убыванию"
    POPULARITY = "По популярности"
    NEW_PRODUCTS = "По новинкам"


class BasketSorterNames(Enum):
    ALL = 'Все'
    PROCCESED = "Только обработанные"
    UNPROCCESED = "Только в ожидание"