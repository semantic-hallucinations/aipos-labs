// Скрипт для изменения текста на странице при нажатии кнопки

// Функция для изменения текста
function changeText() {
    const element = document.getElementById('message');
    if (element) {
        element.textContent = 'Текст изменён!';
    }
}

// Функция для добавления обработчика события
function setupButton() {
    const button = document.getElementById('changeTextButton');
    if (button) {
        button.addEventListener('click', changeText);
    }
}

// Выполняется после загрузки страницы
document.addEventListener('DOMContentLoaded', setupButton);
