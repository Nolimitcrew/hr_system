from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from .models import Contract, WorkYear
from apps.vacations.models import VacationAccrual


@receiver(post_save, sender=Contract)
def create_work_year_and_accrual(sender, instance, created, **kwargs):
    """
    При создании контракта создает Рабочие годы и начисления.
    Работает для контрактов на 1, 2, 3 и более лет.
    """
    if created:
        current_start = instance.start_date
        days_to_accrue = instance.employee.default_vacation_days

        while True:
            # Если контракт срочный и текущий год начинается позже даты окончания - останавливаемся
            if instance.end_date and current_start > instance.end_date:
                break

            # Конец рабочего года - через год минус 1 день
            current_end = current_start + relativedelta(years=1) - timedelta(days=1)

            # Создаем рабочий год
            work_year = WorkYear.objects.create(
                employee=instance.employee,
                start_date=current_start,
                end_date=current_end
            )

            # Начисляем отпуск
            VacationAccrual.objects.create(
                employee=instance.employee,
                work_year=work_year,
                days=days_to_accrue,
                reason="Автоматическое начисление за рабочий год",
                date_accrued=current_start
            )

            # Сдвигаем дату на следующий год для следующей итерации
            current_start = current_start + relativedelta(years=1)