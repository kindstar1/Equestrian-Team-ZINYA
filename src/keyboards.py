from telebot import types

schedule_days = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
]

def generate_schedule_keyboard(selected_items):
    markup = types.InlineKeyboardMarkup()
    for day in schedule_days:
        if day in selected_items:
            text = f"{day} ✅"
        else:
            text = day
        callback_data = f"schedule_{day}"
        markup.add(types.InlineKeyboardButton(text, callback_data=callback_data))
    markup.add(types.InlineKeyboardButton("Готово", callback_data="schedule_done"))
    return markup