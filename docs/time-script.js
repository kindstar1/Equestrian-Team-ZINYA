// 1. Получаем объект WebApp из глобального объекта window
let tg = window.Telegram.WebApp;

// 2. Расширяем Web App на всю высоту
tg.expand();

// 3. Находим наши элементы на странице
const timePicker = document.getElementById('time_picker');
const selectTimeBtn = document.getElementById('select_time_btn');

// 4. Вешаем обработчик на кнопку
selectTimeBtn.addEventListener('click', () => {
    // 5. Получаем значение из поля выбора времени
    const selectedTime = timePicker.value;

    if (selectedTime) {
        // 6. Отправляем данные обратно в бот
        // Это главная магия Web Apps!
        tg.sendData(selectedTime);
        
        // 7. Закрываем окно Web App
        tg.close();
    } else {
        // Показываем нативное уведомление, если время не выбрано
        tg.showAlert('Пожалуйста, выберите время:');
    }
});