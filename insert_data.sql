-- Начало транзакции
BEGIN TRANSACTION;

-- Шаг 1: Очистка таблиц в правильном порядке
DELETE FROM Schedule;
DELETE FROM Subscription;
DELETE FROM Users;
DELETE FROM Horses;
DELETE FROM TrainingTypes;

-- Шаг 2: Базовые данные (Лошади, Типы тренировок)
INSERT INTO Horses (horse_id, horse_name) VALUES
(1, 'Умка'),
(2, 'Зингер'),
(3, 'Государыня');

INSERT INTO TrainingTypes (train_id, training_type) VALUES
(1, 'subscription'),
(2, 'trial');

-- Шаг 3: Пользователи
INSERT INTO Users (user_id, full_name, username, role, status) VALUES
(555000001, 'Елена Смирнова', 'elena_s', 'student', 'active'),
(555000002, 'Дмитрий Волков', 'dmitry_v', 'student', 'active'),
(555000003, 'Мария Лебедева', 'maria_l', 'student', 'active'),
(555000004, 'Андрей Попов', 'andrey_p', 'student', 'active'),
(555000005, 'Светлана Новикова', 'svetlana_n', 'student', 'active');

-- Шаг 4: Абонементы
INSERT INTO Subscription (student_id, purchase_date, end_date, total_sessions, used_sessions, status) VALUES
(555000001, DATE('now', '-20 days'), DATE('now', '+36 days'), 8, 2, 'active'),  -- Использовано 2, осталось 6
(555000002, DATE('now', '-30 days'), DATE('now', '+54 days'), 12, 3, 'active'), -- Использовано 3, осталось 9
(555000003, DATE('now', '-10 days'), DATE('now', '+32 days'), 6, 1, 'active'),  -- Использовано 1, осталось 5
(555000004, DATE('now', '-40 days'), DATE('now', '+16 days'), 8, 4, 'active'),  -- Использовано 4, осталось 4
(555000005, DATE('now'), DATE('now', '+84 days'), 12, 0, 'active');             -- Использовано 0, осталось 12

-- Шаг 5: Полная история тренировок в Schedule

-- == Елена Смирнова (2 прошедших, 6 будущих), sub_id=1 ==
-- Прошедшие занятия
INSERT INTO Schedule (user_id, subscription_id, horse_id, train_id, scheduled_datetime, status, created_at, updated_at) VALUES
(555000001, 1, 1, 1, '2023-10-23 19:00:00', 'completed', DATETIME('now', '-7 days'), DATETIME('now', '-7 days')),
(555000001, 1, 2, 1, '2023-10-25 19:00:00', 'completed', DATETIME('now', '-5 days'), DATETIME('now', '-5 days'));
-- Будущие занятия
INSERT INTO Schedule (user_id, subscription_id, horse_id, train_id, scheduled_datetime, status) VALUES
(555000001, 1, 3, 1, '2023-11-01 19:00:00', 'scheduled'),
(555000001, 1, 1, 1, '2023-11-06 19:00:00', 'scheduled'),
(555000001, 1, 2, 1, '2023-11-08 19:00:00', 'scheduled'),
(555000001, 1, 3, 1, '2023-11-13 19:00:00', 'scheduled'),
(555000001, 1, 1, 1, '2023-11-15 19:00:00', 'scheduled'),
(555000001, 1, 2, 1, '2023-11-20 19:00:00', 'scheduled');

-- == Дмитрий Волков (3 прошедших, 9 будущих), sub_id=2 ==
-- Прошедшие занятия
INSERT INTO Schedule (user_id, subscription_id, horse_id, train_id, scheduled_datetime, status, created_at, updated_at) VALUES
(555000002, 2, 1, 1, '2023-10-20 20:00:00', 'completed', DATETIME('now', '-10 days'), DATETIME('now', '-10 days')),
(555000002, 2, 2, 1, '2023-10-25 20:00:00', 'completed', DATETIME('now', '-5 days'), DATETIME('now', '-5 days')),
(555000002, 2, 3, 1, '2023-10-27 20:00:00', 'completed', DATETIME('now', '-3 days'), DATETIME('now', '-3 days'));
-- Будущие занятия
INSERT INTO Schedule (user_id, subscription_id, horse_id, train_id, scheduled_datetime, status) VALUES
(555000002, 2, 1, 1, '2023-11-01 20:00:00', 'scheduled'),
(555000002, 2, 2, 1, '2023-11-03 20:00:00', 'scheduled'),
(555000002, 2, 3, 1, '2023-11-08 20:00:00', 'scheduled'),
(555000002, 2, 1, 1, '2023-11-10 20:00:00', 'scheduled'),
(555000002, 2, 2, 1, '2023-11-15 20:00:00', 'scheduled'),
(555000002, 2, 3, 1, '2023-11-17 20:00:00', 'scheduled'),
(555000002, 2, 1, 1, '2023-11-22 20:00:00', 'scheduled'),
(555000002, 2, 2, 1, '2023-11-24 20:00:00', 'scheduled'),
(555000002, 2, 3, 1, '2023-11-29 20:00:00', 'scheduled');

-- == Мария Лебедева (1 прошедшее, 5 будущих), sub_id=3 ==
-- Прошедшие занятия
INSERT INTO Schedule (user_id, subscription_id, horse_id, train_id, scheduled_datetime, status, created_at, updated_at) VALUES
(555000003, 3, 3, 1, '2023-10-24 18:30:00', 'completed', DATETIME('now', '-6 days'), DATETIME('now', '-6 days'));
-- Будущие занятия
INSERT INTO Schedule (user_id, subscription_id, horse_id, train_id, scheduled_datetime, status) VALUES
(555000003, 3, 1, 1, '2023-10-31 18:30:00', 'scheduled'),
(555000003, 3, 2, 1, '2023-11-07 18:30:00', 'scheduled'),
(555000003, 3, 3, 1, '2023-11-14 18:30:00', 'scheduled'),
(555000003, 3, 1, 1, '2023-11-21 18:30:00', 'scheduled'),
(555000003, 3, 2, 1, '2023-11-28 18:30:00', 'scheduled');

-- == Андрей Попов (4 прошедших, 4 будущих), sub_id=4 ==
-- Прошедшие занятия
INSERT INTO Schedule (user_id, subscription_id, horse_id, train_id, scheduled_datetime, status, created_at, updated_at) VALUES
(555000004, 4, 1, 1, '2023-10-07 11:00:00', 'completed', DATETIME('now', '-23 days'), DATETIME('now', '-23 days')),
(555000004, 4, 2, 1, '2023-10-14 11:00:00', 'completed', DATETIME('now', '-16 days'), DATETIME('now', '-16 days')),
(555000004, 4, 3, 1, '2023-10-21 11:00:00', 'completed', DATETIME('now', '-9 days'), DATETIME('now', '-9 days')),
(555000004, 4, 1, 1, '2023-10-28 11:00:00', 'completed', DATETIME('now', '-2 days'), DATETIME('now', '-2 days'));
-- Будущие занятия
INSERT INTO Schedule (user_id, subscription_id, horse_id, train_id, scheduled_datetime, status) VALUES
(555000004, 4, 2, 1, '2023-11-04 11:00:00', 'scheduled'),
(555000004, 4, 3, 1, '2023-11-11 11:00:00', 'scheduled'),
(555000004, 4, 1, 1, '2023-11-18 11:00:00', 'scheduled'),
(555000004, 4, 2, 1, '2023-11-25 11:00:00', 'scheduled');

-- == Светлана Новикова (0 прошедших, 12 будущих), sub_id=5 ==
-- Будущие занятия
INSERT INTO Schedule (user_id, subscription_id, horse_id, train_id, scheduled_datetime, status) VALUES
(555000005, 5, 1, 1, '2023-10-31 20:30:00', 'scheduled'),
(555000005, 5, 2, 1, '2023-11-02 20:30:00', 'scheduled'),
(555000005, 5, 3, 1, '2023-11-07 20:30:00', 'scheduled'),
(555000005, 5, 1, 1, '2023-11-09 20:30:00', 'scheduled'),
(555000005, 5, 2, 1, '2023-11-14 20:30:00', 'scheduled'),
(555000005, 5, 3, 1, '2023-11-16 20:30:00', 'scheduled'),
(555000005, 5, 1, 1, '2023-11-21 20:30:00', 'scheduled'),
(555000005, 5, 2, 1, '2023-11-23 20:30:00', 'scheduled'),
(555000005, 5, 3, 1, '2023-11-28 20:30:00', 'scheduled'),
(555000005, 5, 1, 1, '2023-11-30 20:30:00', 'scheduled'),
(555000005, 5, 2, 1, '2023-12-05 20:30:00', 'scheduled'),
(555000005, 5, 3, 1, '2023-12-07 20:30:00', 'scheduled');

-- Завершение транзакции
COMMIT;