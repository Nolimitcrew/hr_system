from django.db import models
from apps.employees.models import Employee


class Contract(models.Model):
    """Трудовой контракт или договор"""

    CONTRACT_TYPES = [
        ('indefinite', 'Бессрочный (на неопределенный срок)'),
        ('fixed', 'Срочный (на определенный срок)'),
        ('temp', 'Временный'),
        ('seasonal', 'Сезонный'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name="Сотрудник"
    )
    contract_number = models.CharField(max_length=50, verbose_name="Номер контракта/договора")
    contract_type = models.CharField(
        max_length=20,
        choices=CONTRACT_TYPES,
        default='fixed',
        verbose_name="Тип контракта"
    )
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата окончания (для срочных)"
    )


    is_active = models.BooleanField(default=True, verbose_name="Действующий")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"
        ordering = ['-start_date']

    def __str__(self):
        return f"Контракт №{self.contract_number} от {self.start_date.strftime('%d.%m.%Y')} ({self.employee.last_name})"


class WorkYear(models.Model):
    """
    Рабочий год сотрудника.
    В отличие от календарного года, он начинается с даты приема на работу.
    Нужен для правильного начисления дней отпуска.
    """
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='work_years',
        verbose_name="Сотрудник"
    )
    start_date = models.DateField(verbose_name="Начало рабочего года")
    end_date = models.DateField(verbose_name="Окончание рабочего года")

    is_closed = models.BooleanField(
        default=False,
        verbose_name="Закрыт",
        help_text="Отметьте, если рабочий год полностью отработан и отпуска за него предоставлены"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Рабочий год"
        verbose_name_plural = "Рабочие годы"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.employee.last_name}: {self.start_date.strftime('%d.%m.%Y')} - {self.end_date.strftime('%d.%m.%Y')}"