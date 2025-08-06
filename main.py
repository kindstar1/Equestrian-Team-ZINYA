from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage

from src.config import TELEGRAM_BOT_TOKEN
from src.handlers.common import commands
from src.handlers.common import register_common_handlers
from src.handlers.faq_child import register_child_faq_handlers
from src.handlers.faq_client import register_client_faq_handlers

state_storage = StateMemoryStorage()

bot = TeleBot(TELEGRAM_BOT_TOKEN, state_storage=state_storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))

register_common_handlers(bot)
register_client_faq_handlers(bot)
register_child_faq_handlers(bot)

bot.set_my_commands(commands=commands)


@bot.message_handler(func=lambda message: True)
def echo_state(message):
    cid = message.chat.id
    tg_id = message.from_user.id
    state = bot.get_state(tg_id, cid)
    bot.send_message(
        cid, f"ОТЛАДКА: Получен текст '{message.text}'. Текущее состояние: {state}"
    )

bot.infinity_polling(skip_pending=True)
