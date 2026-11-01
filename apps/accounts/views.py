from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

from apps.employees.models import Employee
from apps.contracts.models import Contract
from apps.vacations.models import Vacation
from apps.events.models import HREvent
from .forms import CustomUserCreationForm


def home(request):
    """Главная страница (Дашборд)"""
    today = timezone.now().date()

    # 1. Считаем действующих сотрудников
    active_employees = Employee.objects.filter(is_active=True).count()

    # 2. Считаем действующие контракты
    active_contracts = Contract.objects.filter(is_active=True).count()

    # 3. Отпуска в этом месяце (все статусы)
    vacations_this_month = Vacation.objects.filter(
        start_date__year=today.year,
        start_date__month=today.month
    ).count()

    # 4. Последние 5 событий в системе
    recent_events = HREvent.objects.select_related('employee').order_by('-event_date', '-created_at')[:5]

    context = {
        'active_employees_count': active_employees,
        'active_contracts_count': active_contracts,
        'vacations_this_month': vacations_this_month,
        'recent_events': recent_events,
    }
    return render(request, 'home.html', context)


# Вспомогательная проверка: пускаем только суперпользователей
def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def user_list(request):
    """Список всех пользователей системы"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})


@user_passes_test(is_admin)
def user_add_modal(request):
    """Модальное окно добавления пользователя"""
    form = CustomUserCreationForm()
    return render(request, 'accounts/partials/user_modal.html', {'form': form})


@user_passes_test(is_admin)
def user_add_submit(request):
    """Обработка формы добавления пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            response = render(request, 'accounts/partials/user_table.html', {
                'users': User.objects.all().order_by('-date_joined')
            })
            response['HX-Trigger'] = 'closeModal'
            return response
        return render(request, 'accounts/partials/user_modal.html', {'form': form})
    return HttpResponse(status=405)