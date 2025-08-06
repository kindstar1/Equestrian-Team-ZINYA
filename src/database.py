import sqlalchemy
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, date

from models import Base, Horses, Schedule, Subscription, TrainingTypes, TrainingTypeTrainingType, Users, UserRole, UserStatus, SubscriptionStatus, ScheduleStatus

db_file = 'clients.db'
engine = sqlalchemy.create_engine(f'sqlite:///{db_file}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


if __name__ == '__main__':
    print("Создание таблиц в базе данных...")
    
    Base.metadata.create_all(engine)
    
    print(f"✅ База данных '{db_file}' успешно создана/проверена.")
    print("Все таблицы на месте.")

# def get_session():
#     return SessionLocal()

    def generate_test_data():
        # --- Базовые сущности ---
        horse1 = Horses(horse_name="Умка")
        horse2 = Horses(horse_name="Зингер")
        horse3 = Horses(horse_name="Государыня")
        
        training_type_trial = TrainingTypes(training_type=TrainingTypeTrainingType.trial)
        training_type_sub = TrainingTypes(training_type=TrainingTypeTrainingType.subscription)

        # --- Пользователи ---
        admin_user = Users(user_id=111111111, full_name="Иван Петров (Админ)", username="ivan_admin", role=UserRole.admin)
        student_active = Users(user_id=222222222, full_name="Анна Сидорова", username="anna_student", role=UserRole.student)
        student_another = Users(user_id=333333333, full_name="Петр Иванов", username="petr_student", role=UserRole.student)
        student_inactive = Users(user_id=444444444, full_name="Ольга Кузнецова", username="olga_inactive", role=UserRole.student, status=UserStatus.inactive)

        # --- Абонементы ---
        today = date.today()
        
        # Активный абонемент у Анны
        sub_active = Subscription(
            student=student_active,
            purchase_date=today - timedelta(weeks=2),
            end_date=today + timedelta(weeks=6), # 8 недель
            total_sessions=8,
            used_sessions=2,
            status=SubscriptionStatus.active
        )
        
        # Завершенный абонемент у Анны (в прошлом)
        sub_completed = Subscription(
            student=student_active,
            purchase_date=today - timedelta(weeks=12),
            end_date=today - timedelta(weeks=6), # 6 недель
            total_sessions=6,
            used_sessions=6,
            status=SubscriptionStatus.completed
        )

        # Просроченный абонемент у Петра
        sub_expired = Subscription(
            student=student_another,
            purchase_date=today - timedelta(weeks=14),
            end_date=today - timedelta(weeks=2), # 12 недель
            total_sessions=12,
            used_sessions=5,
            status=SubscriptionStatus.expired
        )

        # Замороженный абонемент у Петра
        sub_frozen = Subscription(
            student=student_another,
            purchase_date=today - timedelta(weeks=4),
            end_date=today + timedelta(weeks=4), # 8 недель
            total_sessions=8,
            used_sessions=1,
            status=SubscriptionStatus.frozen
        )

        # --- Расписание ---
        
        # Запланированная тренировка для Анны по активному абонементу
        schedule1 = Schedule(
            user=student_active,
            subscription=sub_active,
            horse=horse1,
            training_type=training_type_sub,
            scheduled_datetime=datetime.now() + timedelta(days=3, hours=2),
            status=ScheduleStatus.scheduled
        )
        
        # Прошедшая (завершенная) тренировка для Анны
        schedule2 = Schedule(
            user=student_active,
            subscription=sub_completed,
            horse=horse2,
            training_type=training_type_sub,
            scheduled_datetime=datetime.now() - timedelta(days=50),
            status=ScheduleStatus.completed
        )

        # Отмененная тренировка для Петра
        schedule3 = Schedule(
            user=student_another,
            subscription=sub_frozen, # по замороженному абонементу
            horse=horse3,
            training_type=training_type_sub,
            scheduled_datetime=datetime.now() - timedelta(days=1),
            status=ScheduleStatus.cancelled
        )

        # Пробная тренировка для нового клиента (без абонемента)
        schedule4 = Schedule(
            user=student_inactive, # неактивный пользователь пришел на пробное
            subscription=None, 
            horse=horse1,
            training_type=training_type_trial,
            scheduled_datetime=datetime.now() + timedelta(days=5),
            status=ScheduleStatus.scheduled
        )

        # Сбор всех объектов для загрузки в БД
        all_data_objects = [
            horse1, horse2, horse3,
            training_type_trial, training_type_sub,
            admin_user, student_active, student_another, student_inactive,
            sub_active, sub_completed, sub_expired, sub_frozen,
            schedule1, schedule2, schedule3, schedule4
        ]
        
        return all_data_objects
    
    data_to_load = generate_test_data()

    try:
        session.add_all(data_to_load)
        session.commit()
        print(f"Успешно загружено {len(data_to_load)} объектов в базу данных.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        session.rollback()
    finally:
        session.close()

