from telebot.handler_backends import State, StatesGroup
import enum
from datetime import datetime
import zoneinfo 

from sqlalchemy import (BigInteger, Column, Date, DateTime, Enum, ForeignKey, Integer, String, Text, Boolean, create_engine)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

months = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
        7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }

class Command:
    SIGNING = "Записаться на пробную тренировку"
    KNOW_COST = "Узнать стоимость"
    GO_TO_MENU = "Возврат в главное меню🔙"
    СONTACT_TO_ZINYA = "Связаться с тренером"
    REQUEST_REVIEW = 'Посмотреть отзывы'
    AGAIN_REQUEST_REVIEW = 'Посмотреть еще отзывы👀'
    SEND_REVIEW = "Оставить отзыв"
    ADD_TO_AWATING_LIST = 'Попасть в лист ожидания'
    CAMP_INFO = "Узнать про детский лагерь"
    NEXT_WORKOUT = "График ближайших тренировок"
    CANCEL_WORKOUT = 'Отменить тренировку'
    RESCHEDULE_WORKOUT = "Перенести тренировку"


class MyStates(StatesGroup):
    greeting = State()
    get_person = State()
    get_name = State()
    get_age = State()
    get_schedule = State()
    get_level = State()
    get_prefers = State()
    get_faq = State()
    get_age_chld = State()
    get_name_chld = State()
    get_level_chld = State()
    parent = State()
    get_name_parent = State()
    client = State()
    get_schedule_chld = State()
    get_time_chld = State()
    get_time = State()
    get_prefers_chld = State()
    support = State()
    awaiting_stars = State() 
    awaiting_text = State() 
    contact_to_yulia = State()
    awaiting_new_workout_day = State()
    awaiting_new_workout_time = State()


Base = declarative_base()

# --- Перечисления (Enums) для полей status ---
MOSCOW_TZ = zoneinfo.ZoneInfo("Europe/Moscow")
def get_moscow_time():
    return datetime.now(MOSCOW_TZ)

class UserRole(enum.Enum):
    admin = "admin"
    student = "student"

class UserStatus(enum.Enum):
    active = "active"
    inactive = "inactive"

class RentStatus(enum.Enum):
    paid = "paid"
    notpaid = "not_paid"
 
class TrainTypeTrainType(enum.Enum):
    trial = 'trial'
    rent = 'rent'

class ScheduleStatus(enum.Enum):
    scheduled = "scheduled"
    rescheduled = 'rescheduled'
    completed = "completed"
    cancelled = "cancelled"

# --- Модели таблиц ---

class Users(Base):
    __tablename__ = 'Users'
    user_id = Column(BigInteger, primary_key=True, autoincrement=False)
    full_name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), nullable=False)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.inactive)
    want_to_camp = Column(Boolean, nullable=False, default=False)

class Rent(Base):
    __tablename__ = 'Rent'
    rent_id = Column(Integer, primary_key=True)
    student_id = Column(BigInteger, ForeignKey('Users.user_id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    rent_status = Column(Enum(RentStatus), nullable=False, default=RentStatus.notpaid)
    amount = Column(Integer, nullable=False)
    horse_id = Column(Integer, ForeignKey('Horses.horse_id'), nullable=False)
    
    student = relationship("Users", backref="rents")
    horse = relationship("Horses", backref="horses")

class Horses(Base):
    __tablename__ = 'Horses'
    horse_id = Column(Integer, primary_key=True)
    horse_name = Column(String(255), nullable=False, unique=True)
    
    schedules = relationship("Schedule", back_populates="horse")

class TrainTypes(Base):
    __tablename__ = 'TrainTypes'
    train_id = Column(Integer, primary_key=True)
    train_type = Column(Enum(TrainTypeTrainType), unique=True, nullable=False)

class Schedule(Base):
    __tablename__ = 'Schedule'
    schedule_id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('Users.user_id'), nullable=False)
    rent_id = Column(Integer, ForeignKey('Rent.rent_id'), nullable=True)
    horse_id = Column(Integer, ForeignKey('Horses.horse_id'), nullable=True)
    train_id = Column(Integer, ForeignKey('TrainTypes.train_id'), nullable=False)
    scheduled_datetime = Column(DateTime, nullable=False)
    train_status = Column(Enum(ScheduleStatus), nullable=False, default=ScheduleStatus.scheduled)
    created_at = Column(DateTime(timezone=True), default=get_moscow_time)
    updated_at = Column(DateTime(timezone=True), default=get_moscow_time, onupdate=get_moscow_time)

    user = relationship("Users", backref="schedules")
    rent = relationship("Rent", backref="schedules")
    horse = relationship("Horses", back_populates="schedules")
    train_type = relationship("TrainTypes", backref="schedules")

class Review(Base):
    __tablename__ = 'Review'
    review_id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=True)
    stars = Column(Integer, nullable=True)
    created_at = created_at = Column(DateTime(timezone=True), default=get_moscow_time)