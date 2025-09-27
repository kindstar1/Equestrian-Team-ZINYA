-- ===================================================================
-- СКРИПТ ДЛЯ ПОЛНОГО ОБНОВЛЕНИЯ ТЕСТОВЫХ ДАННЫХ (ВЕРСИЯ 5)
-- ===================================================================

-- Шаг -1: Очистка старых тестовых данных
-- -------------------------------------------------------------------
DELETE FROM "Schedule" WHERE user_id = 812366187; -- 👈 ЗАМЕНИТЕ НА ВАШ TELEGRAM ID
DELETE FROM "Rent" WHERE student_id = 812366187; -- 👈 ЗАМЕНИТЕ НА ВАШ TELEGRAM ID


-- ===================================================================
-- Шаг 0: Гарантируем наличие типа тренировки 'rent'
-- -------------------------------------------------------------------
INSERT OR IGNORE INTO "TrainTypes" (train_type) VALUES ('rent');


-- ===================================================================
-- Шаг 1: Создание записи об аренде на Сентябрь 2025
-- -------------------------------------------------------------------
INSERT INTO "Rent" (student_id, horse_id, start_date, end_date, rent_status, amount)
VALUES (
    812366187, -- 👈 ЗАМЕНИТЕ НА ВАШ TELEGRAM ID
    (SELECT horse_id FROM "Horses" WHERE horse_name = 'Умка'),
    '2025-09-01',
    '2025-09-30',
    'paid',
    2
);

-- ПОСЛЕ ВЫПОЛНЕНИЯ УЗНАЙТЕ ID СОЗДАННОЙ ЗАПИСИ.
-- В SQLite: SELECT last_insert_rowid();
-- Предположим, вы получили ID = 5. Подставьте его в Шаг 2.
-- ===================================================================


-- Шаг 2: Создание записей в расписании на Сентябрь 2025

INSERT INTO "Schedule" (
    user_id, rent_id, horse_id, train_id, scheduled_datetime, 
    train_status, created_at, updated_at
)
VALUES
    -- Используем datetime(CURRENT_TIMESTAMP, '+3 hours') для получения времени в UTC+3
    (812366187, 5, (SELECT horse_id FROM "Horses" WHERE horse_name = 'Умка'), (SELECT train_id FROM "TrainTypes" WHERE train_type = 'rent'), '2025-09-01 20:00:00', (CASE WHEN '2025-09-01 20:00:00' < datetime(CURRENT_TIMESTAMP, '+3 hours') THEN 'completed' ELSE 'scheduled' END), datetime(CURRENT_TIMESTAMP, '+3 hours'), datetime(CURRENT_TIMESTAMP, '+3 hours')),
    (812366187, 5, (SELECT horse_id FROM "Horses" WHERE horse_name = 'Умка'), (SELECT train_id FROM "TrainTypes" WHERE train_type = 'rent'), '2025-09-04 20:00:00', (CASE WHEN '2025-09-04 20:00:00' < datetime(CURRENT_TIMESTAMP, '+3 hours') THEN 'completed' ELSE 'scheduled' END), datetime(CURRENT_TIMESTAMP, '+3 hours'), datetime(CURRENT_TIMESTAMP, '+3 hours')),
    (812366187, 5, (SELECT horse_id FROM "Horses" WHERE horse_name = 'Умка'), (SELECT train_id FROM "TrainTypes" WHERE train_type = 'rent'), '2025-09-08 20:00:00', (CASE WHEN '2025-09-08 20:00:00' < datetime(CURRENT_TIMESTAMP, '+3 hours') THEN 'completed' ELSE 'scheduled' END), datetime(CURRENT_TIMESTAMP, '+3 hours'), datetime(CURRENT_TIMESTAMP, '+3 hours')),
    (812366187, 5, (SELECT horse_id FROM "Horses" WHERE horse_name = 'Умка'), (SELECT train_id FROM "TrainTypes" WHERE train_type = 'rent'), '2025-09-11 20:00:00', (CASE WHEN '2025-09-11 20:00:00' < datetime(CURRENT_TIMESTAMP, '+3 hours') THEN 'completed' ELSE 'scheduled' END), datetime(CURRENT_TIMESTAMP, '+3 hours'), datetime(CURRENT_TIMESTAMP, '+3 hours')),
    (812366187, 5, (SELECT horse_id FROM "Horses" WHERE horse_name = 'Умка'), (SELECT train_id FROM "TrainTypes" WHERE train_type = 'rent'), '2025-09-15 20:00:00', (CASE WHEN '2025-09-15 20:00:00' < datetime(CURRENT_TIMESTAMP, '+3 hours') THEN 'completed' ELSE 'scheduled' END), datetime(CURRENT_TIMESTAMP, '+3 hours'), datetime(CURRENT_TIMESTAMP, '+3 hours')),
    (812366187, 5, (SELECT horse_id FROM "Horses" WHERE horse_name = 'Умка'), (SELECT train_id FROM "TrainTypes" WHERE train_type = 'rent'), '2025-09-18 20:00:00', (CASE WHEN '2025-09-18 20:00:00' < datetime(CURRENT_TIMESTAMP, '+3 hours') THEN 'completed' ELSE 'scheduled' END), datetime(CURRENT_TIMESTAMP, '+3 hours'), datetime(CURRENT_TIMESTAMP, '+3 hours')),
    (812366187, 5, (SELECT horse_id FROM "Horses" WHERE horse_name = 'Умка'), (SELECT train_id FROM "TrainTypes" WHERE train_type = 'rent'), '2025-09-22 20:00:00', (CASE WHEN '2025-09-22 20:00:00' < datetime(CURRENT_TIMESTAMP, '+3 hours') THEN 'completed' ELSE 'scheduled' END), datetime(CURRENT_TIMESTAMP, '+3 hours'), datetime(CURRENT_TIMESTAMP, '+3 hours')),
    (812366187, 5, (SELECT horse_id FROM "Horses" WHERE horse_name = 'Умка'), (SELECT train_id FROM "TrainTypes" WHERE train_type = 'rent'), '2025-09-25 20:00:00', (CASE WHEN '2025-09-25 20:00:00' < datetime(CURRENT_TIMESTAMP, '+3 hours') THEN 'completed' ELSE 'scheduled' END), datetime(CURRENT_TIMESTAMP, '+3 hours'), datetime(CURRENT_TIMESTAMP, '+3 hours')),
    (812366187, 5, (SELECT horse_id FROM "Horses" WHERE horse_name = 'Умка'), (SELECT train_id FROM "TrainTypes" WHERE train_type = 'rent'), '2025-09-29 20:00:00', (CASE WHEN '2025-09-29 20:00:00' < datetime(CURRENT_TIMESTAMP, '+3 hours') THEN 'completed' ELSE 'scheduled' END), datetime(CURRENT_TIMESTAMP, '+3 hours'), datetime(CURRENT_TIMESTAMP, '+3 hours'))