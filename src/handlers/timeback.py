from telebot import types

# URL, по которому будет доступна ваша веб-страница.
# Мы получим его на следующем шаге. Пока просто оставим как переменную.
WEB_APP_URL = "https://your-username.github.io/your-repo-name/" 


def register_webapp_handlers(bot):
    @bot.message_handler(commands=['select_time'])
    def show_time_selector(message):
        markup = types.InlineKeyboardMarkup()
        
        # Создаем специальную кнопку Web App
        web_app_button = types.InlineKeyboardButton(
            text="Открыть выбор времени", 
            web_app=types.WebAppInfo(url=WEB_APP_URL)
        )
        markup.add(web_app_button)

        bot.send_message(
            message.chat.id, 
            "Нажмите на кнопку ниже, чтобы открыть удобный интерфейс выбора времени.", 
            reply_markup=markup
        )