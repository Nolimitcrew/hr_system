from django.db import models
from django.conf import settings
from apps.employees.models import Employee


class HREvent(models.Model):
    """Кадровое событие (прием, перевод, увольнение и т.д.)"""

    EVENT_TYPES = [
        ('hire', 'Приём на работу'),
        ('transfer', 'Перевод'),
        ('dismissal', 'Увольнение'),
        ('vacation', 'Отпуск'),
        ('sick_leave', 'Больничный'),
        ('other', 'Другое'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='hr_events',
        verbose_name="Сотрудник"
    )
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        verbose_name="Тип события"
    )
    event_date = models.DateField(verbose_name="Дата события")
    description = models.TextField(blank=True, verbose_name="Описание / Примечание")
    document_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Номер приказа/документа"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")

    class Meta:
        verbose_name = "Кадровое событие"
        verbose_name_plural = "Кадровые события"
        ordering = ['-event_date', '-created_at']

    def __str__(self):
        return f"{self.employee.last_name} - {self.get_event_type_display()} ({self.event_date.strftime('%d.%m.%Y')})"


class ChangeLog(models.Model):
    """История изменений (Аудит)"""
    model_name = models.CharField(max_length=100, verbose_name="Название таблицы/модели")
    object_id = models.PositiveIntegerField(verbose_name="ID записи")
    field_name = models.CharField(max_length=100, verbose_name="Измененное поле")
    old_value = models.TextField(blank=True, null=True, verbose_name="Старое значение")
    new_value = models.TextField(blank=True, null=True, verbose_name="Новое значение")

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Кто изменил"
    )
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name="Когда изменил")

    class Meta:
        verbose_name = "История изменений"
        verbose_name_plural = "История изменений"
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.model_name} (ID:{self.object_id}) - {self.field_name} изменено {self.changed_at.strftime('%d.%m.%Y %H:%M')}"