from telebot.apihelper import ApiTelegramException
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta

from src.models import Schedule, ScheduleStatus, MOSCOW_TZ
from src.database import SessionLocal
from sqlalchemy import select

import os

jobstores = {
    'default': SQLAlchemyJobStore(url=os.getenv("DATABASE_URL")) 
}

scheduler = BackgroundScheduler(jobstores=jobstores, timezone=MOSCOW_TZ)

horses_list = ["Умка", "Туман", "Государыня"]

def send_wo_reminder(bot, user_id, horse_name, scheduled_time):
    try:
        if horse_name in horses_list:
            ksk = "КСК Вольт"
        else:
            ksk = "КСК Битца"
        text = (f"🔔Напоминание о тренировке!\n\n"
                f"Ваша тренировка начнется в **{scheduled_time.strftime('%H:%M')}** в {ksk}!"
                f"Юля и {horse_name} будут ждать Вас🐴👩🏼")
        bot.send_message(user_id, text, parse_mode="Markdown")
    except ApiTelegramException as e:
        print(f"Напоминание не было отправлено клиенту c id {user_id}. Ошибка: {e}")
    except Exception as e:
        print(f"❌ Произошла непредвиденная ошибка при отправке напоминания: {e}")

REMIND_HOURS_BEFORE = 2
SCAN_INTERVAL_MINUTES = 15

def schedule_reminder():
    with SessionLocal as ses:
        now = datetime.now(MOSCOW_TZ)
        start = now + timedelta(hours=REMIND_HOURS_BEFORE)
        end = start + timedelta(minutes=SCAN_INTERVAL_MINUTES)

        assoc = select(Schedule).where(Schedule.scheduled_datetime.between(start, end)).where(Schedule.train_status == ScheduleStatus.scheduled)
        wo_list = ses.execute(assoc).scalars().all()

        for wo in wo_list:
            job_id = f"reminder_training_{wo.schedule_id}"
            if scheduler.get_job(job_id):
                print(f"ℹ️ Напоминание для тренировки {wo.schedule_id} уже запланировано. Пропускаем.")
                continue
            reminder_time = wo.scheduled_datetime - timedelta(hours=REMIND_HOURS_BEFORE)

            scheduler.add_job(
                send_wo_reminder,
                trigger='date',
                run_date=reminder_time,
                args=[
                    wo.user_id, wo.scheduled_datetime, wo.horse.horse_name
                ],
                id=job_id,
                replace_existing=True
            )    