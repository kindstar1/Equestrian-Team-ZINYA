from telebot import types
from src.database import SessionLocal
from src.models import Users, UserRole, UserStatus, Review, Schedule, ScheduleStatus
from sqlalchemy import select, and_
from src.models import weekdays, months

schedule_days = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
]

count_stars = {
    1: "⭐",
    2: "⭐⭐",
    3: "⭐⭐⭐",
    4: "⭐⭐⭐⭐",
    5: "⭐⭐⭐⭐⭐",
}

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

def generate_stars_keyboard():
    markup = types.InlineKeyboardMarkup()
    for star in count_stars.keys():
        button_text = count_stars[star]
        callback_data = f"rate_{star}"
        markup.add(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
    return markup

def generate_workout_keyboard(tg_id):
    markup = types.InlineKeyboardMarkup()
    ses = SessionLocal()
    assoc = select(Schedule).join(Schedule.user).where(and_(
        Schedule.user_id == tg_id,
        Schedule.train_status == ScheduleStatus.scheduled))
    workout_list = ses.execute(assoc).scalars().all()
    if not workout_list:
        return None
    for wo in workout_list:
        dt = wo.scheduled_datetime
        day_of_week = weekdays[dt.weekday()]
        month_name = months[dt.month]
        button_text = f"{day_of_week}, {dt.day} {month_name}"
        callback_data = f"workout_select_{wo.schedule_id}"
        markup.add(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
    return markup 

def generate_workout_keyboard_re(tg_id):
    markup = types.InlineKeyboardMarkup()
    ses = SessionLocal()
    assoc = select(Schedule).join(Schedule.user).where(and_(
        Schedule.user_id == tg_id,
        Schedule.train_status == ScheduleStatus.scheduled))
    workout_list = ses.execute(assoc).scalars().all()
    if not workout_list:
        return None
    for wo in workout_list:
        dt = wo.scheduled_datetime
        day_of_week = weekdays[dt.weekday()]
        month_name = months[dt.month]
        button_text = f"{day_of_week}, {dt.day} {month_name}"
        callback_data = f"workout_select2_{wo.schedule_id}"
        markup.add(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
    return markup 
    
    
    
        



