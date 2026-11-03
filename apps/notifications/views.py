from django.shortcuts import render
from django.http import HttpResponse
from apps.notifications.services import send_telegram_message


def telegram_test_modal(request):
    """Возвращает модальное окно для проверки Telegram"""
    return render(request, 'notifications/partials/telegram_modal.html')


def telegram_test_submit(request):
    """Отправляет сообщение и возвращает результат"""
    if request.method == 'POST':
        text = request.POST.get('message', 'Тестовое сообщение из HR-Системы')

        # Вызываем нашу функцию отправки
        success, message = send_telegram_message(text)

        # Передаем результат в шаблон
        context = {
            'success': success,
            'message': message,
            'text': text
        }
        return render(request, 'notifications/partials/telegram_result.html', context)
    return HttpResponse(status=405)