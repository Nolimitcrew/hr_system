from django.db import models
from apps.employees.models import Employee
from apps.contracts.models import WorkYear


class VacationAccrual(models.Model):
    """Начисление отпускных дней за конкретный рабочий год"""
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='vacation_accruals',
        verbose_name="Сотрудник"
    )
    work_year = models.ForeignKey(
        WorkYear,
        on_delete=models.PROTECT,
        related_name='accruals',
        verbose_name="Рабочий год"
    )
    days = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Начислено дней"
    )
    reason = models.CharField(
        max_length=200,
        verbose_name="Основание",
        help_text="Например: 'Основной отпуск за рабочий год'"
    )
    date_accrued = models.DateField(verbose_name="Дата начисления")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Начисление отпуска"
        verbose_name_plural = "Начисления отпусков"
        ordering = ['-date_accrued']

    def __str__(self):
        return f"{self.employee.last_name} - {self.days} дн. ({self.reason})"


class Vacation(models.Model):
    """Запись об отпуске (запланированном или фактическом)"""

    VACATION_TYPES = [
        ('trud', 'Трудовой (основной)'),
        ('soc', 'Социальный'),
        ('bez', 'За свой счет (без сохранения з/п)'),
        ('uch', 'Учебный'),
    ]

    STATUS_CHOICES = [
        ('planned', 'Запланирован'),
        ('actual', 'Фактический (использован)'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='vacations',
        verbose_name="Сотрудник"
    )
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    days = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Количество календарных дней"
    )
    vacation_type = models.CharField(
        max_length=20,
        choices=VACATION_TYPES,
        default='trud',
        verbose_name="Тип отпуска"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned',
        verbose_name="Статус"
    )
    document_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Номер приказа"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Отпуск"
        verbose_name_plural = "Отпуска"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.employee.last_name}: отпуск {self.start_date.strftime('%d.%m.%Y')} - {self.end_date.strftime('%d.%m.%Y')} ({self.get_status_display()})"