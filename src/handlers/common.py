from telebot import types

from src.models import Command
from src.models import Command, MyStates
from src.config import SUPPORT_BOT


commands = [
    types.BotCommand("menu", "Меню"),
    types.BotCommand("help", "Справка: что умеет бот"), # предлагаются кнопки записаться на занятие, инфо по абонементу, купить абонемент
    types.BotCommand("info", "Информация о команде"), # будут предлагаться узнать стоимость и обратную связь и связаться с тренером, детский лагерь
    types.BotCommand("location", "Где мы находимся"),
    types.BotCommand("review", "Абонементы"), # кнопки продумать - возможно инфо и продление
    types.BotCommand("review", "Детский лагерь"), # ссылка на Юлин сайт? возможно предзапись в лист ожидания - в админке продумать вызов всей инфы по записавшимся
    types.BotCommand("review", "Обратная связь"), # будут предлагаться кнопки остаивть отзыв и посмотреть отзывы (лонгридом) и связаться с тренером
    types.BotCommand("support", "Связаться с тех.поддержкой"), # написать АБ по проблеме работы бота
    types.BotCommand("restart", "Перезапустить бота")
]

markup_remover = types.ReplyKeyboardRemove()

def back_to_menu(bot, message):
    cid = message.chat.id
    tg_id = message.from_user.id
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # btn1 = types.KeyboardButton("Записаться на занятие")
    # btn2 = types.KeyboardButton("Узнать стоимость")
    # btn3 = types.KeyboardButton("Детский лагерь")
    # markup.add(btn1, btn2, btn3)
    bot.send_message(cid, "Вы в главном меню. Что Вас интересует?", reply_markup=markup_remover)
    # bot.delete_state(str(tg_id), str(cid))
    bot.delete_state(tg_id, cid)

def register_common_handlers(bot):
    @bot.message_handler(commands=["start"])
    def greeting(message):
        tg_name = message.from_user.first_name
        cid = message.chat.id
        bot.send_message(
            cid,
            f"Привет, {tg_name}! Я бот команды ZINYA EQ. Чтобы узнать, что я умею, открой меню🔽",
        )

    @bot.message_handler(func=lambda message: message.text == Command.KNOW_COST)
    def cost_info(message):
        cid = message.chat.id
        bot.send_message(
            cid,
            "Стоимость пробного занятия - 5000 руб.\nДалее работа ведется по абонементу: \n- 6 занятий - 28 800 руб. (тренировка 4 800 руб.)\n- 8 занятий - 36’000 (тренировка 4’500)\n- 10 занятий - 42’000 (тренировка 4’200)\n- 12 занятий - 48’000 (тренировка 4’000)\nСроки действия - 6, 8, 10 и 12 недель соответственно. На период отъездов или болезни абонементы замораживаются", reply_markup=markup_remover
        )
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Записаться на занятие")
        btn2 = types.KeyboardButton("Возврат в главное меню")
        markup.add(btn1, btn2)
        bot.send_message(cid, "Выбери действие:", reply_markup=markup)

    @bot.message_handler(state=MyStates.support)
    def save_support_request(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        username = message.from_user.username
        text = message.text
        if "/" in text:
            bot.delete_state(tg_id, cid)
        else:
            with bot.retrieve_data(tg_id, cid) as data:
                data["support_req"] = message.text
                support_message = (
                    f"🚨 Новое обращение в тех.поддержку!\n\n"
                    f"Ник в тг: {username}\n"
                    f"ID пользователя: {tg_id}\n"
                    "----------------------------------\n"
                    f"Описание проблемы: {data.get('support_req')}\n"
                    )
                bot.send_message(SUPPORT_BOT, support_message)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton("Возврат в главное меню")
            markup.add(btn1)
            bot.send_message(
                cid,
                "Ваш запрос принят! В ближайшее время тех. сециалист его рассмотрит и устранит неполадки.",
                reply_markup=markup
            )
            bot.delete_state(tg_id, cid)


    @bot.message_handler(state=MyStates.get_faq)
    def handle_faq_answer(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        if message.text == "Нет":
            bot.send_message(cid, "Возвращайтесь, как будете готовы :)")
            bot.delete_state(tg_id, cid)
            back_to_menu(message)
        elif message.text == "Да":
            with bot.retrieve_data(tg_id, cid) as data:
                check_id_client = data.get("id")
            if check_id_client == tg_id:
                bot.send_message(
                    cid, "Ваши ответы уже сохранены, дождитесь, пока тренер свяжется с Вами"
                )
            else:
                markup = types.ReplyKeyboardMarkup(
                    resize_keyboard=True, one_time_keyboard=True
                )
                btn1 = types.KeyboardButton("Я")
                btn2 = types.KeyboardButton("Ребенок")
                markup.add(btn1, btn2)
                bot.send_message(
                    cid,
                    "Кто планирует заниматься: Вы или Ваш ребенок?",
                    reply_markup=markup,
                )
                bot.set_state(tg_id, MyStates.get_person, cid)
        else:
            bot.send_message(cid, "Команда не распознана, пожалуйста, используйте кнопки.")


    @bot.message_handler(state=MyStates.get_person)
    def info_client(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        if message.text == "Я":
            with bot.retrieve_data(tg_id, cid) as data:
                data["person"] = "Запрос сформирован всадником"
            bot.send_message(cid, "Как Вас зовут?")
            bot.set_state(tg_id, MyStates.client, cid)
        elif message.text == "Ребенок":
            with bot.retrieve_data(tg_id, cid) as data:
                data["person"] = (
                    "Запрос сформирован родителем. Заниматься планирует ребенок"
                )
            bot.send_message(cid, "Как Вас зовут?")
            bot.set_state(tg_id, MyStates.parent, cid)
        elif message.text == "Возврат в главное меню":
            back_to_menu(message)
            bot.delete_state(tg_id, cid)

    @bot.message_handler(func=lambda message: message.text == Command.SIGNING)
    def signing(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        bot.set_state(tg_id, MyStates.get_faq, cid)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        btn3 = types.KeyboardButton("Возврат в главное меню")
        markup.add(btn1, btn2, btn3)
        bot.send_message(
            cid,
            "Для записи необходимо ответить на пару вопросов. Готовы?",
            reply_markup=markup,
        )

    @bot.message_handler(func=lambda message: message.text == Command.GO_TO_MENU)
    def return_to_menu_button(message):
        back_to_menu(bot, message)
    
    @bot.message_handler(commands=["menu"])
    def menu(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        bot.send_message(cid, "Вы в главном меню. Что Вас интересует?", reply_markup=markup_remover)
        bot.delete_state(tg_id, cid)
    
    @bot.message_handler(commands=["info"])
    def info_about_team(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        bot.delete_state(tg_id, cid)
        photo_paths = [
        'src/images/юля.png',
        'src/images/sobina.png',
        'src/images/sobina2.png']
        try:
            media = []
            for path in photo_paths:
                file = open(path, 'rb')
                media.append(types.InputMediaPhoto(file))
            if media:
                bot.send_media_group(chat_id=cid, media=media)
        except Exception as e:
            print(f"ОШИБКА: Произошла непредвиденная ошибка при отправке фото: {e}")
        info_text = """Занимаюсь с теми, кому неинтересно «катание» на лошади, кто хочет научиться грамотно работать средствами управления и в последующем развиваться в спорте (в том числе любительском).На тренировке вы не остаётесь один на один с лошадью, на протяжении всего занятия получаете множество комментариев и упражнений для отработки.

Вот несколько примеров того, что мы с учениками осваиваем на тренировках: баланс и ритм лошади, импульс, проводимость, работа со сгибаниями, постановлениями, полуодержками, расслабление лошади под верхом, дистанции и расчет в конкуре, подъезд к барьеру, построение прыжковой посадки, работу мягкой и «живой» рукой, навык «чувствовать» лошадь; выявляем зажимы в посадке и постепенно их устраняем.

<b>В каких случаях мы сработаемся?</b>
✅ Если у вас есть стремление освоить конный спорт на более глубоком уровне, открыть для себя тончайший мир многогранного взаимодействия с лошадью.
✅ Если подход тренера «раз в 10 минут дать указание о смене аллюра» вас совершенно не устраивает.
✅ Если вы хотите научиться качественно прыгать, считать дистанции и видеть расчёт.
✅ Если вы хотите развиваться именно в спорте (в том числе любительском), а не кататься на лошади.

Также однозначно смогу вам помочь, если после неудачного падения вы испытываете страх при езде верхом, но хотите от него избавиться.

🏆 По мере подготовки всадника возможны выезды на старты. 

🏕️Дважды в год провожу детский конный лагерь в Подмосковье.

<b>👩🏼Коротко обо мне:</b>
В конном спорте на протяжении 15 лет. Тренирую на своем высоком (172 см в холке) и абсолютно безопасном мерине латвийской породы.
Обучалась в том числе за границей, на базе конно-спортивных клубов Германии и Австрии."""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("Узнать стоимость")
        btn2 = types.KeyboardButton("Почитать отзывы")
        btn3 = types.KeyboardButton("Связаться с тренером")
        btn4 = types.KeyboardButton("Узнать про детский лагерь")
        btn5 = types.KeyboardButton("Возврат в главное меню")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(
            cid,
            info_text,
            reply_markup=markup, parse_mode='HTML'
        )
    
    @bot.message_handler(commands=["support"])
    def get_support(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        tg_name = message.from_user.first_name
        bot.delete_state(tg_id, cid)
        bot.send_message(
            cid,
            f"Привет, {tg_name}! Это тех.поддержка бота ZINYA. Опиши, пожалуйста, что случилось? Если при использовании бота ты заметил проблему/ошибку - расскажи мне о ней:", 
            reply_markup=markup_remover
        )
        bot.set_state(tg_id, MyStates.support, cid)
    
    @bot.message_handler(commands=['location'])
    def get_location(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        bot.delete_state(tg_id, cid)
        markup = types.InlineKeyboardMarkup()
        location_button = types.InlineKeyboardButton(text="Посмотреть на карте", url='https://yandex.ru/maps/-/CHdj788V')
        markup.add(location_button) 
        try:
            with open('src/images/Битца.jpg', 'rb') as photo:
                bot.send_photo(
                    chat_id=cid,
                    photo=photo, caption="Занятия проходят в КСК Битца📍 (ст.м. Чертановская)", reply_markup=markup)
        except Exception as e:
            print(f"Ошибка: {e}. Не удалось загрузить картнку, шаг пропущен")
       
        





