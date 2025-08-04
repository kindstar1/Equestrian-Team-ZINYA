from telebot.handler_backends import State, StatesGroup


class Command:
    SIGNING = "Записаться на занятие"
    KNOW_COST = "Узнать стоимость"
    GO_TO_MENU = "Возврат в главное меню"
    СONTACT_TO_ZINYA = "Связаться с тренером"
    REVIEWS = "Связаться с тренером"


class MyStates(StatesGroup):
    get_person = State()
    get_name = State()
    get_age = State()
    get_schedule = State()
    get_level = State()
    get_prefers = State()
    get_faq = State()
    get_age_chld = State()
    get_name_chld = State()
    get_level_chld = State()
    parent = State()
    get_name_parent = State()
    client = State()
    get_schedule_chld = State()
    get_time_chld = State()
    get_time = State()
    get_prefers_chld = State()
    support = State()