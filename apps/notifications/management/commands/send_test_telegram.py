from django.core.management.base import BaseCommand
from apps.notifications.services import send_telegram_message


class Command(BaseCommand):
    help = 'Отправляет тестовое сообщение в Telegram'

    def handle(self, *args, **kwargs):
        self.stdout.write("Отправляем тестовое сообщение...")

        success, message = send_telegram_message(
            "<b>Привет!</b> Это тестовое сообщение из HR-Системы. Интеграция работает!"
        )

        if success:
            self.stdout.write(self.style.SUCCESS(f"Успех! {message}"))
        else:
            self.stdout.write(self.style.ERROR(f"Ошибка! {message}"))