import time
from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from apps.notifications.tasks import daily_checks


class Command(BaseCommand):
    help = 'Запускает планировщик для ежедневных проверок'

    def handle(self, *args, **kwargs):
        scheduler = BlockingScheduler()

        # Запускаем задачу каждый день в 09:00 утра
        scheduler.add_job(daily_checks, 'cron', hour=9, minute=0)

        self.stdout.write(self.style.SUCCESS("Планировщик запущен. Ожидание задач... (Ctrl+C для выхода)"))

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.stdout.write(self.style.WARNING("\nПланировщик остановлен."))