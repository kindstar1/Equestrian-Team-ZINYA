import os
import threading
from flask import Flask
import time

from src.handlers.common import commands
from src.handlers.common import register_common_handlers
from src.handlers.faq_child import register_child_faq_handlers
from src.handlers.faq_client import register_client_faq_handlers
from src.handlers.debug_handler import register_debug_handlers
from src.handlers.admin.main_panel import register_common_admin_handlers
from src.handlers.scheduler import scheduler, schedule_reminder, SCAN_INTERVAL_MINUTES


from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from src.config import TELEGRAM_BOT_TOKEN
from src.filters import IsAdminFilter


# Код для веб-сервера, который нужен для бесплатного тарифа Render
app = Flask(__name__)


@app.route("/")
def health_check():
    return "OK"


def run_web_server():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# ---

state_storage = StateMemoryStorage()
bot = TeleBot(TELEGRAM_BOT_TOKEN, state_storage=state_storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(IsAdminFilter())

print("Bot is starting...")

register_common_handlers(bot)
register_client_faq_handlers(bot)
register_child_faq_handlers(bot)
register_debug_handlers(bot)
register_common_admin_handlers(bot)


bot.set_my_commands(commands=commands)


@bot.message_handler(func=lambda message: True)
def echo_state(message):
    cid = message.chat.id
    tg_id = message.from_user.id
    state = bot.get_state(tg_id, cid)
    bot.send_message(
        cid, f"ОТЛАДКА: Получен текст '{message.text}'. Текущее состояние: {state}"
    )


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    scheduler.add_job(
        schedule_reminder,
        "interval",
        minutes=SCAN_INTERVAL_MINUTES,
        id="main_reminder_scanner",
        replace_existing=True,
    )

    # Запускаем планировщик
    scheduler.start()
    print("▶️ Планировщик задач запущен.")

    while True:
        try:
            print("Starting infinity polling...")
            bot.infinity_polling(skip_pending=True)
        except Exception as e:
            print(f"Ловим ошибку: {e}")
            print("Restarting in 5 seconds...")
            time.sleep(5)
