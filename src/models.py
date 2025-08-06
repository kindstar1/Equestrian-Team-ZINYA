from telebot.handler_backends import State, StatesGroup
import enum
from datetime import datetime, timedelta

from sqlalchemy import (BigInteger, Column, Date, DateTime, Enum, ForeignKey, Integer, String, create_engine)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Command:
    SIGNING = "Записаться на занятие"
    KNOW_COST = "Узнать стоимость"
    GO_TO_MENU = "Возврат в главное меню"
    СONTACT_TO_ZINYA = "Связаться с тренером"
    REVIEWS = ""


class MyStates(StatesGroup):
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

Base = declarative_base()

# --- Перечисления (Enums) для полей status ---

class UserRole(enum.Enum):
    admin = "admin"
    student = "student"

class UserStatus(enum.Enum):
    active = "active"
    inactive = "inactive"

class SubscriptionStatus(enum.Enum):
    active = "active"
    completed = "completed"
    frozen = 'frozen'
    expired = "expired"

class TrainingTypeTrainingType(enum.Enum):
    trial = 'trial'
    subscription = 'subscription'

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
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.active)

class Subscription(Base):
    __tablename__ = 'Subscription'
    subscription_id = Column(Integer, primary_key=True)
    student_id = Column(BigInteger, ForeignKey('Users.user_id'), nullable=False)
    purchase_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_sessions = Column(Integer, nullable=False)
    used_sessions = Column(Integer, nullable=False, default=0)
    status = Column(Enum(SubscriptionStatus), nullable=False, default=SubscriptionStatus.active)
    
    student = relationship("Users", backref="subscriptions")

class Horses(Base):
    __tablename__ = 'Horses'
    horse_id = Column(Integer, primary_key=True)
    horse_name = Column(String(255), nullable=False, unique=True)
    
    schedules = relationship("Schedule", back_populates="horse")

class TrainingTypes(Base):
    __tablename__ = 'TrainingTypes'
    train_id = Column(Integer, primary_key=True)
    training_type = Column(Enum(TrainingTypeTrainingType), nullable=False, default=TrainingTypeTrainingType.subscription)

class Schedule(Base):
    __tablename__ = 'Schedule'
    schedule_id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('Users.user_id'), nullable=False)
    subscription_id = Column(Integer, ForeignKey('Subscription.subscription_id'), nullable=True)
    horse_id = Column(Integer, ForeignKey('Horses.horse_id'), nullable=True)
    train_id = Column(Integer, ForeignKey('TrainingTypes.train_id'), nullable=False)
    
    scheduled_datetime = Column(DateTime, nullable=False)
    status = Column(Enum(ScheduleStatus), nullable=False, default=ScheduleStatus.scheduled)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("Users", backref="schedules")
    subscription = relationship("Subscription", backref="schedules")
    horse = relationship("Horses", back_populates="schedules")
    training_type = relationship("TrainingTypes", backref="schedules")