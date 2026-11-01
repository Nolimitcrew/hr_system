from django.db import models
from django.conf import settings
from apps.employees.models import Employee


class TelegramNotification(models.Model):
    """Очередь уведомлений для отправки в Telegram"""

    STATUS_CHOICES = [
        ('pending', 'Ожидает отправки'),
        ('sent', 'Отправлено'),
        ('error', 'Ошибка'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Сотрудник (если связано)"
    )
    recipient_chat_id = models.CharField(max_length=50, verbose_name="ID чата в Telegram")
    message = models.TextField(verbose_name="Текст сообщения")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Отправлено")

    class Meta:
        verbose_name = "Уведомление Telegram"
        verbose_name_plural = "Уведомления Telegram"
        ordering = ['-created_at']

    def __str__(self):
        return f"Сообщение для {self.recipient_chat_id} ({self.get_status_display()})"


class ActionLog(models.Model):
    """Журнал действий пользователей в системе"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )
    action = models.CharField(max_length=255, verbose_name="Действие")
    details = models.TextField(blank=True, verbose_name="Детали")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время")

    class Meta:
        verbose_name = "Журнал действий"
        verbose_name_plural = "Журнал действий"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.action} ({self.timestamp.strftime('%d.%m.%Y %H:%M')})"