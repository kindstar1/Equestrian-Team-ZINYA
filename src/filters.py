from telebot.custom_filters import SimpleCustomFilter
from telebot.types import Message

from src.database import SessionLocal
from src.models import Users, UserRole

class IsAdminFilter(SimpleCustomFilter):
    """
    Проверяет, является ли пользователь администратором.
    Ключ для использования в хендлерах: `is_admin`
    """
    key = 'is_admin'

    def check(self, message: Message):
        user_id = message.from_user.id
        
        with SessionLocal() as session:
            user = session.get(Users, user_id)
            
            if not user or user.role != UserRole.admin:
                return False
        return True