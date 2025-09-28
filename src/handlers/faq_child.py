from telebot import types
from src.models import MyStates
from src.keyboards import generate_schedule_keyboard
from src.handlers.common import back_to_menu
from src.config import ADMIN_ID
from src.handlers.common import markup_remover

# Цепочка вопросов для сбора информаии о ребенке
def register_child_faq_handlers(bot):
    @bot.message_handler(state=MyStates.parent)
    def get_name_child(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        with bot.retrieve_data(tg_id, cid) as data:
            data["parent_name"] = message.text
        bot.send_message(cid, "Как зовут Вашего ребенка? Введите имя:", reply_markup=markup_remover)
        bot.set_state(tg_id, MyStates.get_name_chld, cid)


    @bot.message_handler(state=MyStates.get_name_chld)
    def get_age_child(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        with bot.retrieve_data(tg_id, cid) as data:
            data["child_name"] = message.text
        bot.send_message(cid, "Сколько лет Вашему ребенку? Введите цифру:")
        bot.set_state(tg_id, MyStates.get_age_chld, cid)


    @bot.message_handler(state=MyStates.get_age_chld)
    def get_level_child(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        with bot.retrieve_data(tg_id, cid) as data:
            data["child_age"] = message.text
        if int(message.text) < 8:
            parent_name = data.get("parent_name")
            bot.send_message(
                cid,
                f"❗{parent_name}, для детей младше 8-ми лет потребуется отдельное собеседование с тренером для понимания, сможет ли ребенок тренироваться на лошади, а не пони!",
            )
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
            btn1 = types.KeyboardButton("Нет опыта верховой езды")
            btn2 = types.KeyboardButton("Начальный: шаг")
            btn3 = types.KeyboardButton("Средний: шаг + рысь")
            btn4 = types.KeyboardButton("Продвинутый: все 3 аллюра")
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(
                cid, "Какой уровень верховой езды у Вашего ребенка?", reply_markup=markup
            )
            bot.set_state(tg_id, MyStates.get_level_chld, cid)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
            btn1 = types.KeyboardButton("Нет опыта верховой езды")
            btn2 = types.KeyboardButton("Начальный: шаг")
            btn3 = types.KeyboardButton("Средний: шаг + рысь")
            btn4 = types.KeyboardButton("Продвинутый: все 3 аллюра")
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(
                cid, "Какой уровень верховой езды у Вашего ребенка?", reply_markup=markup
            )
            bot.set_state(tg_id, MyStates.get_level_chld, cid)


    @bot.message_handler(state=MyStates.get_level_chld)
    def get_schedule_child(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        with bot.retrieve_data(tg_id, cid) as data:
            data["child_level"] = message.text
        ask_for_schedule_child(message)


    @bot.callback_query_handler(state=MyStates.get_schedule_chld, func=lambda call: True)
    def child_schedule_selection(call):
        cid = call.message.chat.id
        tg_id = call.from_user.id
        with bot.retrieve_data(tg_id, cid) as data:
            selected = data.get("selected_schedule", [])
            if call.data == "schedule_done":
                if not selected:
                    # Отвечаем на callback, чтобы убрать "часики" на кнопке
                    bot.answer_callback_query(
                        call.id,
                        "Пожалуйста, выберите хотя бы один вариант.",
                        show_alert=True,
                    )
                    return
                bot.send_message(cid, "Напишите удобное время для занятий в формате чч:мм:")
                bot.set_state(tg_id, MyStates.get_time_chld, cid)
                return
            item_name = call.data.split("_")[1]

            if item_name in selected:
                selected.remove(item_name)  # Если уже выбран - убираем
            else:
                selected.append(item_name)  # Если не выбран - добавляем
            data["selected_schedule"] = selected
            updated_markup = generate_schedule_keyboard(selected)
            bot.edit_message_reply_markup(
                chat_id=cid, message_id=call.message.message_id, reply_markup=updated_markup
            )


    @bot.message_handler(state=MyStates.get_time_chld)
    def get_prefers_child(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        with bot.retrieve_data(tg_id, cid) as data:
            data["child_time"] = message.text
        bot.send_message(
            cid,
            "Дополнительная информация о Вашем ребенке: желаемая специализация, травмы, страхи и др.",
        )
        bot.set_state(tg_id, MyStates.get_prefers_chld, cid)


    @bot.message_handler(state=MyStates.get_prefers_chld)
    def end_faq_child(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        username = message.from_user.username
        markup = types.InlineKeyboardMarkup()
        sign_button = types.InlineKeyboardButton("Записать на пробную тренировку", callback_data=f"trial_signup:{tg_id}")
        markup.add(sign_button)
        # ДОПИСАТЬ КОД С КНОКОЙ ЗАПИСАТЬ НА ПРОБНУЮ ТРЕНИРОВКУ
        with bot.retrieve_data(tg_id, cid) as data:
            data["child_prefers"] = message.text
            if username:
                user_info = f"(@{username})"
            admin_message = (
                f"🔔 Новая заявка на занятие!\n\n"
                f"Ник в тг: @{user_info}\n"
                f"ID пользователя: {tg_id}\n"
                "----------------------------------\n"
                f"{data.get('person')}\n"
                f"Имя родителя: {data.get('parent_name', 'не указано')}\n"
                f"Имя ребенка: {data.get('child_name', 'не указано')}\n"
                f"Возраст ребенка: {data.get('child_age', 'не указано')}\n"
                f"Уровень: {data.get('child_level', 'не указано')}\n"
                f"Дни недели: {', '.join(data.get('selected_schedule', ['не указано']))}\n"
                f"Время: {data.get('child_time', 'не указано')}\n"
                f"Предпочтения: {data.get('child_prefers', 'нет')}"
                )
            bot.send_message(ADMIN_ID, admin_message, reply_markup=markup)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Возврат в главное меню🔙")
        markup.add(btn1)
        bot.send_message(
            cid,
            "Опрос пройден! Благодарю за Ваши ответы. В ближайшее время тренер с Вами свяжется!",
            reply_markup=markup,
        )
        bot.delete_state(tg_id, cid)


    def ask_for_schedule_child(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        with bot.retrieve_data(tg_id, cid) as data:
            data["selected_schedule"] = []
        initial_markup = generate_schedule_keyboard([])
        bot.send_message(
            cid,
            "Выберите удобные дни недели для занятий (можно несколько вариантов)\nСначала нажмите на дни недели, в которые удобно посещать занятия, затем нажмите на кнопку 'Готово'",
            reply_markup=initial_markup,
        )
        bot.set_state(tg_id, MyStates.get_schedule_chld, cid)