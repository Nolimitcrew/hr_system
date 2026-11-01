from django.db.models import Sum


def get_vacation_summary(employee):
    """
    Рассчитывает баланс отпускных дней для сотрудника.
    Возвращает словарь с начисленными, использованными, запланированными и доступными днями.
    """
    # Суммируем все начисления
    accrued = employee.vacation_accruals.aggregate(total=Sum('days'))['total'] or 0

    # Суммируем фактические (использованные) отпуска
    used = employee.vacations.filter(status='actual').aggregate(total=Sum('days'))['total'] or 0

    # Суммируем запланированные отпуска
    planned = employee.vacations.filter(status='planned').aggregate(total=Sum('days'))['total'] or 0

    # Свободный остаток = Начислено - Использовано - Запланировано
    available = accrued - used - planned

    return {
        'accrued': accrued,
        'used': used,
        'planned': planned,
        'available': available,
    }