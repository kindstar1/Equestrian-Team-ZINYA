
from telebot import types

from src.models import MyStates
from src.keyboards import generate_schedule_keyboard
from src.handlers.common import back_to_menu
from src.config import ADMIN_ID
from src.handlers.common import markup_remover

allure_list = [
    "Нет опыта верховой езды",
    "Начальный: шаг",
    "Средний: шаг + рысь",
    "Продвинутый: все 3 аллюра"
]


def register_client_faq_handlers(bot):

    # Цепочка вопросов для сбора информаии о взрослом
    @bot.message_handler(state=MyStates.client)
    def get_age_client(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        with bot.retrieve_data(tg_id, cid) as data:
            data["client_name"] = message.text
        bot.send_message(cid, "Cколько Вам лет? Введите цифру:")
        bot.set_state(tg_id, MyStates.get_age, cid)


    @bot.message_handler(state=MyStates.get_age)
    def get_level_client(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        with bot.retrieve_data(tg_id, cid) as data:
            data["client_age"] = message.text
        if int(message.text) < 12:
            client_name = data.get("client_name")
            bot.send_message(
                cid,
                f"❗{client_name}, тренер запросит контакт родителей для обсуждения условий занятий!",
            )
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            btn1 = types.KeyboardButton("Нет опыта верховой езды")
            btn2 = types.KeyboardButton("Начальный: шаг")
            btn3 = types.KeyboardButton("Средний: шаг + рысь")
            btn4 = types.KeyboardButton("Продвинутый: все 3 аллюра")
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(cid, "Какой у Вас уровень верховой езды?", reply_markup=markup)
            bot.set_state(tg_id, MyStates.get_level, cid)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True,  row_width=2)
            btn1 = types.KeyboardButton("Нет опыта верховой езды")
            btn2 = types.KeyboardButton("Начальный: шаг")
            btn3 = types.KeyboardButton("Средний: шаг + рысь")
            btn4 = types.KeyboardButton("Продвинутый: все 3 аллюра")
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(cid, "Какой у Вас уровень верховой езды?", reply_markup=markup)
            bot.set_state(tg_id, MyStates.get_level, cid)


    @bot.message_handler(state=MyStates.get_level)
    def get_scheduled(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        if message.text not in allure_list:
            bot.send_message(cid, "Команда не распознана, пожалуйста, используйте кнопки.")
        else:
            with bot.retrieve_data(tg_id, cid) as data:
                data["client_level"] = message.text
            ask_for_schedule(message)


    @bot.callback_query_handler(state=MyStates.get_schedule, func=lambda call: True)
    def schedule_selection_client(call):
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
                bot.set_state(tg_id, MyStates.get_time, cid)
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


    @bot.message_handler(state=MyStates.get_time)
    def get_prefers(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        with bot.retrieve_data(tg_id, cid) as data:
            data["client_time"] = message.text
        bot.send_message(
            cid,
            "Дополнительная информация о Ваc: желаемая специализация, травмы, страхи и др.",
        )
        bot.set_state(tg_id, MyStates.get_prefers, cid)


    @bot.message_handler(state=MyStates.get_prefers)
    def end_faq_client(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        username = message.from_user.username
        markup = types.InlineKeyboardMarkup()
        sign_button = types.InlineKeyboardButton("Записать на пробную тренировку", callback_data=f"trial_signup:{tg_id}")
        markup.add(sign_button)
        with bot.retrieve_data(tg_id, cid) as data:
            data["client_prefers"] = message.text
            if username:
                user_info = f"(@{username})"
            admin_message = (
                f"🔔 Новая заявка на занятие!\n\n"
                f"Ник в тг: @{user_info}\n"
                f"ID пользователя: {tg_id}\n"
                "----------------------------------\n"
                f"{data.get('person')}\n"
                f"Имя клиента: {data.get('client_name', 'не указано')}\n"
                f"Возраст клиента: {data.get('client_age', 'не указано')}\n"
                f"Уровень: {data.get('client_level', 'не указано')}\n"
                f"Дни недели: {', '.join(data.get('selected_schedule', ['не указано']))}\n"
                f"Время: {data.get('client_time', 'не указано')}\n"
                f"Предпочтения: {data.get('client_prefers', 'нет')}"
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

    def ask_for_schedule(message):
        cid = message.chat.id
        tg_id = message.from_user.id
        with bot.retrieve_data(tg_id, cid) as data:
            data["selected_schedule"] = []
        initial_markup = generate_schedule_keyboard([])
        bot.send_message(
            cid,
            "Выберите удобные дни недели для занятий (можно несколько вариантов), затем нажмите на кнопку 'Готово'",
            reply_markup=initial_markup,
        )
        bot.set_state(tg_id, MyStates.get_schedule, cid)