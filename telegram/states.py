from aiogram.fsm.state import State, StatesGroup


class WelcomeStates(StatesGroup):
    contact = State()

class SenderStates(StatesGroup):
    create_post = State()
    is_done = State()

class OrderStates(StatesGroup):
    region = State()
    name = State()
    phone_number = State()
    quantity = State()