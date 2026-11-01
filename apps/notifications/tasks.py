from datetime import date
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from apps.employees.models import Employee, Child
from apps.contracts.models import Contract, WorkYear
from apps.vacations.models import Vacation, VacationAccrual
from apps.notifications.services import send_telegram_message

def daily_checks():
    """Ежедневная проверка дней рождения, контрактов и графиков отпусков"""
    today = date.today()
    messages = []

    # 1. Дни рождения сотрудников
    birthday_employees = Employee.objects.filter(
        is_active=True, birth_date__month=today.month, birth_date__day=today.day
    )
    for emp in birthday_employees:
        messages.append(f"🎉 Сегодня день рождения у сотрудника: <b>{emp.last_name} {emp.first_name}</b>")

    # 2. Дни рождения детей
    birthday_children = Child.objects.filter(
        employee__is_active=True, birth_date__month=today.month, birth_date__day=today.day
    )
    for child in birthday_children:
        messages.append(f"🎈 Сегодня день рождения у ребенка сотрудника <b>{child.employee.last_name}</b>: {child.full_name}")

    # 3. Окончание контрактов (за 30 дней)
    warning_date = today + relativedelta(days=30)
    expiring_contracts = Contract.objects.filter(
        is_active=True, end_date__lte=warning_date, end_date__gte=today
    ).select_related('employee')
    for contract in expiring_contracts:
        days_left = (contract.end_date - today).days
        messages.append(f"⚠️ Контракт №{contract.contract_number} (<b>{contract.employee.last_name}</b>) заканчивается {contract.end_date.strftime('%d.%m.%Y')}")

    # 4. КОНТРОЛЬ ГРАФИКА ОТПУСКОВ (5-й и 11-й месяц рабочего года)
    active_work_years = WorkYear.objects.filter(
        employee__is_active=True,
        start_date__lte=today,
        end_date__gte=today
    ).select_related('employee')

    for wy in active_work_years:
        # Вычисляем точные даты наступления 5-го и 11-го месяца
        month_5 = wy.start_date + relativedelta(months=4)
        month_11 = wy.start_date + relativedelta(months=10)

        # Считаем, сколько дней начислено за этот год
        total_accrued = VacationAccrual.objects.filter(work_year=wy).aggregate(total=Sum('days'))['total'] or wy.employee.default_vacation_days

        # Считаем, сколько фактически использовано (берем отпуска, которые начались в этом рабочем году)
        used_days = Vacation.objects.filter(
            employee=wy.employee,
            status='actual',
            start_date__gte=wy.start_date,
            end_date__lte=wy.end_date
        ).aggregate(total=Sum('days'))['total'] or 0

        # Проверка на 5-м месяце (первая половина)
        if today == month_5:
            half_vacation = total_accrued / 2
            if used_days < half_vacation:
                messages.append(f"📢 <b>{wy.employee.last_name}</b>: наступил 5-й месяц рабочего года. Использовано {used_days} из {total_accrued} дн. Не забудьте про первую половину отпуска!")

        # Проверка на 11-м месяце (остаток)
        elif today == month_11:
            remaining = total_accrued - used_days
            if remaining > 1: # Если осталось больше 1 дня
                messages.append(f"⏳ <b>{wy.employee.last_name}</b>: до конца рабочего года остался месяц. Осталось {remaining} дн. отпуска (из {total_accrued}).")

    # Отправка в Telegram
    if messages:
        text = "<b>📋 Утренняя сводка HR-Системы:</b>\n\n" + "\n".join(messages)
        success, error = send_telegram_message(text)
        if success:
            print(f"[{today}] Сводка отправлена. Событий: {len(messages)}")
        else:
            print(f"[{today}] Ошибка отправки: {error}")
    else:
        print(f"[{today}] Проверка завершена. Событий нет.")