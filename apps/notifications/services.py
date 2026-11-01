import requests
from django.conf import settings
from django.utils import timezone  # <-- Добавлен импорт
from .models import TelegramNotification


def send_telegram_message(text, chat_id=None):
    """Отправляет сообщение в Telegram и логирует результат в БД"""
    from apps.directories.models import OrganizationSettings

    org = OrganizationSettings.objects.first()
    if not org or not org.telegram_bot_token:
        return False, "В настройках организации не указан токен бота."

    token = org.telegram_bot_token
    target_chat_id = chat_id or org.telegram_chat_id

    if not target_chat_id:
        return False, "Не указан ID чата (Chat ID)."

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": target_chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("ok"):
            TelegramNotification.objects.create(
                recipient_chat_id=str(target_chat_id),
                message=text,
                status='sent',
                sent_at=timezone.now()  # <-- ИСПРАВЛЕНО ТУТ
            )
            return True, "Успешно отправлено"
        else:
            return False, data.get("description", "Неизвестная ошибка API Telegram")

    except requests.exceptions.RequestException as e:
        TelegramNotification.objects.create(
            recipient_chat_id=str(target_chat_id),
            message=text,
            status='error'
        )
        return False, str(e)