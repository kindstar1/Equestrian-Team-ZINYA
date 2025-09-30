from sqlalchemy import select, func, and_

from src.database import SessionLocal

from src.models import Command, MyStates, MOSCOW_TZ, weekdays, months
from src.models import Users, UserRole, UserStatus, Review, Schedule, ScheduleStatus
from telebot import types
from datetime import datetime, timedelta


admin_commands = [
    types.BotCommand("schedule", "Мое расписание 🕓"),
    types.BotCommand("payment", "Оплата аренды 💰"), 
    types.BotCommand("horse", "Мои лошади 🏇🏿"),
    types.BotCommand("wait_camp", "Лист ожидания лагеря ⛺"), 
    types.BotCommand("my_review", "Обратная связь 💬"), # посмотреть или удалить отзыв
]

def register_common_admin_handlers(bot):

    @bot.message_handler(commands=['admin'], is_admin=True)
    def admin_main_panel(message):
        bot.send_message(
            message.chat.id, 
            "Добро пожаловать в панель администратора!"
        )
        bot.set_my_commands(
                            commands=admin_commands, 
                            scope=types.BotCommandScopeChat(message.chat.id))