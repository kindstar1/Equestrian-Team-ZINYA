from sqlalchemy import select, func, and_

from src.database import SessionLocal

from src.keyboards import generate_stars_keyboard
from src.models import Command
from src.models import Command, MyStates
from src.config import SUPPORT_BOT, ADMIN_ID
from src.models import Users, UserRole, UserStatus, Review
from telebot import types

commands = [
    types.BotCommand("menu", "Меню"),
    types.BotCommand("sign", "Записаться на пробную тренировку ✍🏻"),
    types.BotCommand("info", "Информация о команде 📝"), # будут предлагаться узнать стоимость и обратную связь и связаться с тренером, детский лагерь
    types.BotCommand("location", "Где мы находимся 📍"),
    types.BotCommand("trainings", "Мои тренировки 🏇🏿"), 
    types.BotCommand("camp", "Детский лагерь ⛺"), # ссылка на Юлин сайт? возможно предзапись в лист ожидания - в админке продумать вызов всей инфы по записавшимся
    types.BotCommand("review", "Обратная связь 💬"), # будут предлагаться кнопки остаивть отзыв и посмотреть отзывы (лонгридом)
    types.BotCommand("support", "Связаться с тех.поддержкой ⛑"), # написать АБ по проблеме работы бота
]
cmd_str= [
    '/menu',
    '/sign',
    '/info',
    '/location',
    '/trainings',
    '/camp',
    '/review',
    '/support',
]

markup_remover = types.ReplyKeyboardRemove()

def back_to_menu(bot, message):
    cid = message.chat.id
    tg_id = message.from_user.id
    bot.send_message(cid, "Вы в главном меню. Что Вас интересует?", reply_markup=markup_remover)
    bot.delete_state(tg_id, cid)

def start_signing_flow(bot, message):
    cid = message.chat.id
    tg_id = message.from_user.id
    bot.set_state(tg_id, MyStates.get_faq, cid)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("Да")
    btn2 = types.KeyboardButton("Нет")
    btn3 = types.KeyboardButton("Узнать стоимость")
    btn4 = types.KeyboardButton("Возврат в главное меню🔙")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(
        cid,
        "Для записи необходимо ответить на пару вопросов. Готовы?",
        reply_markup=markup,
    )

def request_review(bot, message):
        tg_id = message.from_user.id
        cid = message.chat.id
        ses = SessionLocal()
        random_func = func.random()
        stmt = select(Review).where(and_(
            Review.stars >= 4,
            Review.text.is_not(None),  
            Review.text != '')).order_by(random_func).limit(1)
        random_review = ses.execute(stmt).scalar_one_or_none()
        review_text = f"Оценка {'⭐' * random_review.stars}\n\n" \
                          f"\"{random_review.text}\""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Посмотреть еще отзывы👀")
        btn2 = types.KeyboardButton("Возврат в главное меню🔙")
        markup.add(btn1, btn2)
        bot.send_message(cid, review_text, reply_markup=markup)
        ses.close()

def know_info_about_camp(bot, message):
        cid = message.chat.id
        tg_id = message.from_user.id
        bot.delete_state(tg_id, cid)
        markup = types.InlineKeyboardMarkup()
        zinyacamp = types.InlineKeyboardButton(text="Узнать больше про лагерь", url='https://zinyacamp.ru/#start')
        markup.add(zinyacamp)
        try:
            with open('src/images/camp_z.png', 'rb') as photo:
                bot.send_photo(
                    chat_id=cid,
                    photo=photo, caption="Два раза в год команда проводит детский лагерь для начинающих и профессиональных всадников🐎", reply_markup=markup)
        except Exception as e:
            print(f"Ошибка: {e}. Не удалось загрузить картнку, шаг пропущен")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("Попасть в лист ожидания")
        btn2 = types.KeyboardButton("Возврат в главное меню🔙")
        markup.add(btn1, btn2)
        bot.send_message(
            cid, 'Выбери действие:', 
            reply_markup=markup)


def register_common_handlers(bot):


    @bot.message_handler(state=MyStates.greeting)
    def remember_user(message):
        ses = SessionLocal()
        tg_name = message.from_user.first_name
        tg_id = message.from_user.id
        cid = message.chat.id
        with bot.retrieve_data(tg_id, cid) as data:
            data["full_name"] = message.text
        full_name = data["full_name"]
        if tg_id == 111111111:
            user = Users(user_id=tg_id, full_name=full_name, username = tg_name, role = UserRole.admin)
            bot.send_message(cid,
            f"Привет, Юля! Ты зашла в админку бота. Открой меню для просмотра доступных функций🔽")
            ses.add(user)
            ses.commit()
        else:
            user = Users(user_id=tg_id, full_name=full_name, username = tg_name, role = UserRole.student, status = UserStatus.inactive)
            ses.add(user)
            ses.commit()
            bot.send_message(
                cid,
                f"Регистрация пройдена успешно! Чтобы узнать, что я умею, открой меню🔽",
            )
        bot.delete_state(tg_id, cid)


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
            btn1 = types.KeyboardButton("Возврат в главное меню🔙")
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
            back_to_menu(bot, message)
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
        elif message.text == "Узнать стоимость":
            cost_info(message)
        elif message.text == "Возврат в главное меню🔙":
            back_to_menu(bot, message)
        else:
            bot.send_message(cid, "Команда не распознана, пожалуйста, используйте кнопки.")


    @bot.message_handler(state=MyStates.get_person)
    def info_client(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        if message.text == "Я":
            with bot.retrieve_data(tg_id, cid) as data:
                data["person"] = "Запрос сформирован всадником"
            bot.send_message(cid, "Как Вас зовут?", reply_markup=markup_remover)
            bot.set_state(tg_id, MyStates.client, cid)
        elif message.text == "Ребенок":
            with bot.retrieve_data(tg_id, cid) as data:
                data["person"] = (
                    "Запрос сформирован родителем. Заниматься планирует ребенок"
                )
            bot.send_message(cid, "Как Вас зовут?")
            bot.set_state(tg_id, MyStates.parent, cid)
        elif message.text == "Возврат в главное меню🔙":
            back_to_menu(bot, message)
            bot.delete_state(tg_id, cid)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('rate_'), state=MyStates.awaiting_stars)
    def handle_stars(call):
        cid = call.message.chat.id
        uid = call.from_user.id
        stars = int(call.data.split('_')[1])
        with bot.retrieve_data(uid, cid) as data:
            data['stars'] = stars   
        bot.answer_callback_query(call.id, f"Ваша оценка: {'⭐' * stars}")
        if stars <= 2:
            text = "Расскажите, что пошло не так?"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
            btn = types.KeyboardButton("Возврат в главное меню🔙")
            markup.add(btn)
            bot.send_message(cid, text, reply_markup=markup)
            bot.set_state(uid, MyStates.awaiting_text, cid)         
        else:    
            text = "Теперь, пожалуйста, напишите отзыв текстом"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
            btn = types.KeyboardButton("Возврат в главное меню🔙")
            markup.add(btn)
            bot.send_message(cid, text, reply_markup=markup)
            bot.set_state(uid, MyStates.awaiting_text, cid)

    @bot.message_handler(state=MyStates.awaiting_text)
    def handle_review_text(message):
        cid = message.chat.id
        uid = message.from_user.id
        review_text = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
        btn = types.KeyboardButton("Возврат в главное меню🔙")
        markup.add(btn)
    
        with bot.retrieve_data(uid, cid) as data:
            stars = data.get('stars', None) 
        if stars is None:
            bot.send_message(cid, "Произошла ошибка, попробуйте начать заново: /review", reply_markup=markup)
            return
        ses = SessionLocal()
        if review_text == "Возврат в главное меню🔙":
            try:
                new_review = Review(
                    stars=stars)
                ses.add(new_review)
                ses.commit()
                bot.send_message(cid, "✅ Спасибо! Ваша оценка успешно сохранена.")
                back_to_menu(bot, message)
            except Exception as e:
                ses.rollback()
                bot.send_message(cid, "❌ Произошла ошибка при сохранении оценки.", reply_markup=markup)
            finally:
                ses.close()
        elif review_text in cmd_str:
            try:
                new_review = Review(
                    stars=stars)
                ses.add(new_review)
                ses.commit()
                bot.send_message(cid, "✅ Спасибо! Ваша оценка успешно сохранена.\nВызовите команду повторно, пожалуйста")
            except Exception as e:
                ses.rollback()
                bot.send_message(cid, "❌ Произошла ошибка при сохранении оценки.", reply_markup=markup)
            finally:
                ses.close()
        
        else:
            try:
                new_review = Review(
                    stars=stars,
                    text=review_text
                )
                ses.add(new_review)
                ses.commit()
                bot.send_message(cid, "✅ Спасибо! Ваши оценка и отзыв успешно сохранены.", reply_markup=markup)
            except Exception as e:
                ses.rollback()
                bot.send_message(cid, "❌ Произошла ошибка при сохранении отзыва.", reply_markup=markup)
            finally:
                ses.close()
        bot.delete_state(uid, cid)

    @bot.message_handler(state=MyStates.contact_to_yulia)
    def handle_contact_text(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        text = message.text 
        with bot.retrieve_data(tg_id, cid) as data:
            data["request"] = text
        username = message.from_user.username
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Возврат в главное меню🔙")
        markup.add(btn1)
        if text == "Возврат в главное меню🔙":
            bot.send_message(cid,"Отменил запрос.",)
            back_to_menu(bot, message)
        elif text in cmd_str:
            bot.send_message(
                cid,
                "Отменил запрос. Вызовите, пожалуйста, команду повторно")
        else:    
            admin_message = (
                f"📝С тобой хочет связаться ученик!\n\n"
                f"Ник в тг: @{username}\n"
                "----------------------------------\n"
                f"Суть запроса: {data.get('request', 'не указано')}")
            bot.send_message(ADMIN_ID, admin_message)
            bot.send_message(
                cid,
                "Принято! Я все уже передал тренеру. Ожидайте🙂",
                reply_markup=markup,
            )
        bot.delete_state(tg_id, cid)

#  Хендлеры для кнопок меню

    @bot.message_handler(commands=["start"])
    def greeting(message):
        ses = SessionLocal()
        tg_id = message.from_user.id
        cid = message.chat.id
        user = ses.query(Users).filter_by(user_id=tg_id).first()
        if user is None:
            bot.send_message(cid,
            f"Привет! Я бот команды ZINYA EQ. Представься, пожалуйста: ")
            bot.set_state(tg_id, MyStates.greeting, cid)
        else:
            bot.send_message(cid,
            f"С возвращением! Чтобы выбрать действие, открой меню🔽")
    

    @bot.message_handler(commands=["sign"])
    def signing_from_command(message):
        start_signing_flow(bot, message)
    
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
        btn2 = types.KeyboardButton("Записаться на пробную тренировку")
        btn3 = types.KeyboardButton("Связаться с тренером")
        btn4 = types.KeyboardButton("Узнать про детский лагерь")
        btn5 = types.KeyboardButton("Возврат в главное меню🔙")
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
        markup_volte = types.InlineKeyboardMarkup()
        markup_bitza = types.InlineKeyboardMarkup()
        
        location_button_2 = types.InlineKeyboardButton(text="Посмотреть на карте", url='https://yandex.ru/maps/-/CLeWB4or')
        markup_volte.add(location_button_2) 
        try:
            with open('src/images/volte.png', 'rb') as photo:
                bot.send_photo(
                    chat_id=cid,
                    photo=photo, caption="Занятия проходят в КСК Вольт📍 (Москва, пос.Остафьева)", reply_markup=markup_volte)
        except Exception as e:
            print(f"Ошибка: {e}. Не удалось загрузить картнку, шаг пропущен")
       
        location_button = types.InlineKeyboardButton(text="Посмотреть на карте", url='https://yandex.ru/maps/-/CHdj788V')
        markup_bitza.add(location_button) 
        try:
            with open('src/images/Битца.jpg', 'rb') as photo:
                bot.send_photo(
                    chat_id=cid,
                    photo=photo, caption="А также в КСК Битца📍 (ст.м. Чертановская)", reply_markup=markup_bitza)
        except Exception as e:
            print(f"Ошибка: {e}. Не удалось загрузить картнку, шаг пропущен")
        
        
# Функция просмотра своих занятий

    @bot.message_handler(commands=["trainings"])
    def my_trainings(message):
        ses = SessionLocal()
        cid = message.chat.id
        tg_id = message.from_user.id

# Функция оставить\посмотреть отзывы
    @bot.message_handler(commands=["review"])
    def review(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("Посмотреть отзывы")
        btn2 = types.KeyboardButton("Оставить отзыв")
        markup.add(btn1, btn2)
        bot.send_message(
            cid, 'Выбери действие:', 
            reply_markup=markup, parse_mode='HTML'
        )
# Функция Узнать инфо про детский лагерь
    @bot.message_handler(commands=["camp"])
    def info_about_camp_from_menu(message):
       know_info_about_camp(bot, message)
        
# Самые общие хендлеры

    @bot.message_handler(func=lambda message: message.text == Command.SIGNING)
    def signing_from_button(message):
        start_signing_flow(bot, message)

    
    @bot.message_handler(func=lambda message: message.text == Command.KNOW_COST)
    def cost_info(message):
        tg_id = message.from_user.id
        cid = message.chat.id
        bot.send_message(
            cid,
            "Стоимость пробного занятия - 5000 руб.\nДалее работа ведется по абонементу: \n- 6 занятий - 28 800 руб. (тренировка 4 800 руб.)\n- 8 занятий - 36’000 (тренировка 4’500)\n- 10 занятий - 42’000 (тренировка 4’200)\n- 12 занятий - 48’000 (тренировка 4’000)\nСроки действия - 6, 8, 10 и 12 недель соответственно. На период отъездов или болезни абонементы замораживаются", reply_markup=markup_remover
        )
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Записаться на пробную тренировку")
        btn2 = types.KeyboardButton("Возврат в главное меню🔙")
        markup.add(btn1, btn2)
        bot.send_message(cid, "Выбери действие:", reply_markup=markup)
        bot.delete_state(tg_id, cid)

    @bot.message_handler(func=lambda message: message.text == Command.GO_TO_MENU)
    def return_to_menu_button(message):
        back_to_menu(bot, message)

    @bot.message_handler(func=lambda message: message.text == Command.REQUEST_REVIEW)
    def request_review_from_menu(message):
        request_review(bot, message)
    
    @bot.message_handler(func=lambda message: message.text == Command.AGAIN_REQUEST_REVIEW)
    def request_review_again(message):
        request_review(bot, message)

    @bot.message_handler(func=lambda message: message.text == Command.SEND_REVIEW)
    def send_review(message):
        cid = message.chat.id
        text = 'Оцените тренера, выбрав количество звезд: '
        bot.send_message(cid, text, reply_markup=generate_stars_keyboard())
        tg_id = message.from_user.id
        bot.set_state(tg_id, MyStates.awaiting_stars, cid)

    @bot.message_handler(func=lambda message: message.text == Command.ADD_TO_AWATING_LIST)
    def end_faq_client(message):
        tg_id = message.from_user.id
        cid = message.chat.id
        username = message.from_user.username
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Возврат в главное меню🔙")
        markup.add(btn1)
        ses = SessionLocal()
        user = ses.get(Users, tg_id)
        if user.want_to_camp: 
            bot.send_message(cid, "Вы уже добавлены в лист ожидания... Когда информация появится, команда с Вами свяжется!", reply_markup=markup,)
        else:
            admin_message = (
            f"🔔⛺Новая заявка в лист ожидания!\n\n"
            f"Ник в тг: @{username}\n"
            "----------------------------------\n")
            bot.send_message(ADMIN_ID, admin_message)
            user.want_to_camp = True
            ses.commit()
            ses.close()
            bot.send_message(
            cid,
            "Вы добавлены в лист ожидания! Когда появится обновленная информация про лагерь, команда свяжется с Вами!",
            reply_markup=markup,)


    @bot.message_handler(func=lambda message: message.text == Command.CAMP_INFO)
    def info_capm_from_team(message):
        know_info_about_camp(bot, message)

    @bot.message_handler(func=lambda message: message.text == Command.СONTACT_TO_ZINYA)
    def contact_to_yulia(message):
        cid = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Возврат в главное меню🔙")
        markup.add(btn1)
        text = 'Что мне передать тренеру? Напиши ниже✍🏻'
        bot.send_message(cid, text, reply_markup=markup)
        tg_id = message.from_user.id
        bot.set_state(tg_id, MyStates.contact_to_yulia, cid)      
