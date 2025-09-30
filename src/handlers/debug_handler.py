
from src.models import Users, UserRole
from src.database import SessionLocal
from telebot import types
from src.handlers.admin.main_panel import admin_commands
from src.handlers.common import commands


def register_debug_handlers(bot):

    DEVELOPER_ID = 812366187

    @bot.message_handler(commands=['setrole'])
    def set_my_role(message):
        # --- Шаг 2: Критически важная проверка безопасности! ---
        # Убеждаемся, что команду использует только разработчик
        if message.from_user.id != DEVELOPER_ID:
            bot.reply_to(message, "⛔️ Эта команда доступна только разработчику.")
            return

        # --- Шаг 3: Парсим команду ---
        # Ожидаем команду в формате "/setrole admin" или "/setrole student"
        command_parts = message.text.split()
        if len(command_parts) < 2:
            bot.reply_to(message, "Пожалуйста, укажите роль. Пример: `/setrole student`", parse_mode="Markdown")
            return

        new_role_str = command_parts[1].lower() 

        # --- Шаг 4: Валидация роли ---
        if new_role_str not in [role.value for role in UserRole]:
            bot.reply_to(message, f"Неверная роль '{new_role_str}'. Доступные роли: `admin`, `student`.", parse_mode="Markdown")
            return

        # --- Шаг 5: Обновляем запись в базе данных ---
        try:
            with SessionLocal() as session:
                # Находим пользователя-разработчика в БД
                user_to_update = session.query(Users).filter(Users.user_id == DEVELOPER_ID).first()
                
                if user_to_update:
                    # Меняем роль
                    user_to_update.role = new_role_str
                    session.commit()

                    if new_role_str == 'admin':
                        bot.set_my_commands(
                            commands=admin_commands, 
                            scope=types.BotCommandScopeChat(message.chat.id)
                        )
                    else: # student
                        bot.set_my_commands(
                            commands=commands, 
                            scope=types.BotCommandScopeChat(message.chat.id))
                    
                    # Отправляем подтверждение
                    success_message = (
                        f"✅ Ваша роль успешно изменена на **{new_role_str}**"
                    )
                    bot.reply_to(message, success_message, parse_mode="Markdown")
                else:
                    bot.reply_to(message, "Ваш пользователь не найден в базе данных. Сначала отправьте /start.")
        
        except Exception as e:
            print(f"Ошибка при смене роли: {e}")
            bot.reply_to(message, "❌ Произошла ошибка при обновлении роли в базе данных.")