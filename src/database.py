# import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, date
from src.config import DATABASE_URL
from src.models import Base, Horses, Schedule, Rent, TrainTypes, TrainTypeTrainType, Users, UserRole, UserStatus, RentStatus, ScheduleStatus, Review


engine = sqlalchemy.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

if __name__ == '__main__':
    print("Создание таблиц в базе данных...")
    
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    print("✅ База данных PostgreSQL готова к работе.")
    print("Все таблицы на месте.")

    def generate_const_data():
        # --- Базовые сущности ---
        horse1 = Horses(horse_name="Умка")
        horse2 = Horses(horse_name="Зингер")
        horse3 = Horses(horse_name="Государыня")
        horse4 = Horses(horse_name="Туман")
        
        train_type_trial = TrainTypes(train_type=TrainTypeTrainType.trial)
        train_type_sub = TrainTypes(train_type=TrainTypeTrainType.rent)

        review_1 = Review(text = 
                          """Хочется сказать что самое главное в жизни спортсмена - это тренер. Много лет я искала тренера, с которым смогу развиваться, и наконец то я нашла его. 
Юля прекрасный тренер, объясняет понятным языком, не повышает голос, всегда поддерживает, радуется и грустит вместе с тобой. Она всегда за развитие всадника и лошади.
Когда то я думала, что никогда не сработаюсь с кобылой, как же я ошибалась) Ася очень честная, ласковая и добрая кобыла. Всегда выручит и поможет, а после тренировки почешется об тебя:) 
С ней я поднимала высоты, вышла на свои первые старты и даже сдала на разряд.""",
                          stars = 5)
        review_2 = Review(text = 
                          """Если вы начинающий, средний или уверенный всадник который хочет найти своего тренера, то с Юлией у вас это более чем получится. 
Юля терпеливый, приятный и весёлый тренер. Она всё доходчиво объясняет и рассказывает, а Зюзя просто прелестный конь. 
Всё ещё ходим к Юле и хотелось бы сказать ей спасибо за прекрасные тренеровки. Юлия вы лучший тренер!!""",
                          stars = 5)
        review_3 = Review(text = 
                          """Найти своего тренера - это настоящее счастье!Пришла к Юле на пробную тренировку после неудачного опыта и травм. 
Пришла и осталась, поняла, что не хочу искать ни другого тренера ни коня. Занимаюсь уже год и буду заниматься дальше. 
Юля супер тренер, профессионал своего дела, вежливая, тактичная, дает очень много информации, внимательна к нюансам, все расскажет, поддержит и поможет бороться со страхами и зажимами. 
Таких тренеров сейчас крайне мало.Юля человек с добрым сердцем, который любит своих лошадей и учеников. 
Благодаря такому подходу у меня есть прогресс в тренировках. Каждое занятие, гамма эмоций и счастья. Ну и конечно же Зингер, это просто любовь! 
Высокий, большой, такой ласковый и добрый конь, идеальный учитель.Просто в самое сердце ♥️""",
                          stars = 5)
        review_4 = Review(text = 
                          """Все понравилось, лошадь хорошо обученная и безопасная""",
                          stars = 5)
        
        review_5 = Review(text = 
                          """Спасибо большое Юлие за тренировку. Дочке очень понравилась, сказала, что наконец то мне всё объясняют. Разница огромная с просто прокатом. Лошади у Юли замечательные! 
Будем с удовольствием продолжать тренировки. А ещё Юля рассказала как чистить и седлать лошадь, и дала Наташе во всём этом поучаствовать.""",
                          stars = 5)
        review_6 = Review(text = 
                          """Юля - лучший тренер! Кайфую от каждой тренировки.🔥Зингер-прекрасная лошадь,с огромным сердцем 🫶🏻.""",
                          stars = 5)

        # Сбор всех объектов для загрузки в БД
        all_data_objects = [
            horse1, horse2, horse3, horse4,
            train_type_trial, train_type_sub,
            review_1, review_2, review_3, review_4, review_5, review_6
        ]
        
        return all_data_objects
    
    data_to_load = generate_const_data()

    try:
        session.add_all(data_to_load)
        session.commit()
        print(f"Успешно загружено {len(data_to_load)} объектов в базу данных.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        session.rollback()
    finally:
        session.close()

