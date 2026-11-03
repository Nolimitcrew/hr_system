from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from apps.employees.models import Employee
from .models import VacationAccrual, Vacation
from .forms import VacationAccrualForm, VacationForm
from .services import get_vacation_summary

from django.db.models import Q


def vacation_global_list(request):
    """Глобальная страница со всеми отпусками"""
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    # Берем все отпуска, сразу подтягиваем данные сотрудников (select_related)
    vacations = Vacation.objects.select_related('employee').order_by('-start_date')

    # Фильтр по ФИО
    if query:
        vacations = vacations.filter(
            Q(employee__last_name__icontains=query) |
            Q(employee__first_name__icontains=query) |
            Q(employee__middle_name__icontains=query)
        )

    # Фильтр по статусу
    if status_filter:
        vacations = vacations.filter(status=status_filter)

    context = {
        'vacations': vacations,
        'query': query,
        'status_filter': status_filter,
    }
    return render(request, 'vacations/global_list.html', context)






# --- Начисления ---
def accrual_add_modal(request, employee_pk):
    employee = get_object_or_404(Employee, pk=employee_pk)
    form = VacationAccrualForm(employee=employee)
    return render(request, 'vacations/partials/accrual_modal.html', {'form': form, 'employee': employee})


def accrual_add_submit(request, employee_pk):
    employee = get_object_or_404(Employee, pk=employee_pk)
    if request.method == 'POST':
        form = VacationAccrualForm(request.POST, employee=employee)
        if form.is_valid():
            accrual = form.save(commit=False)
            accrual.employee = employee
            accrual.save()

            # Обновляем всю вкладку отпусков
            return _render_vacation_tab(request, employee)
        return render(request, 'vacations/partials/accrual_modal.html', {'form': form, 'employee': employee})
    return HttpResponse(status=405)


# --- Отпуска ---
def vacation_add_modal(request, employee_pk):
    employee = get_object_or_404(Employee, pk=employee_pk)
    form = VacationForm()
    return render(request, 'vacations/partials/vacation_modal.html', {'form': form, 'employee': employee})


def vacation_add_submit(request, employee_pk):
    employee = get_object_or_404(Employee, pk=employee_pk)
    if request.method == 'POST':
        form = VacationForm(request.POST)
        if form.is_valid():
            vacation = form.save(commit=False)
            vacation.employee = employee
            vacation.save()

            return _render_vacation_tab(request, employee)
        return render(request, 'vacations/partials/vacation_modal.html', {'form': form, 'employee': employee})
    return HttpResponse(status=405)


# --- Вспомогательная функция для обновления вкладки ---
def _render_vacation_tab(request, employee):
    # Пересчитываем баланс и получаем списки
    summary = get_vacation_summary(employee)
    accruals = employee.vacation_accruals.all().order_by('-date_accrued')
    vacations = employee.vacations.all().order_by('-start_date')

    response = render(request, 'vacations/partials/vacation_tab.html', {
        'employee': employee,
        'summary': summary,
        'accruals': accruals,
        'vacations': vacations
    })
    response['HX-Trigger'] = 'closeModal'
    return response

# --- Редактирование и удаление Начислений ---
def accrual_edit_modal(request, accrual_pk):
    accrual = get_object_or_404(VacationAccrual, pk=accrual_pk)
    form = VacationAccrualForm(instance=accrual, employee=accrual.employee)
    return render(request, 'vacations/partials/accrual_edit_modal.html', {'form': form, 'accrual': accrual})

def accrual_edit_submit(request, accrual_pk):
    accrual = get_object_or_404(VacationAccrual, pk=accrual_pk)
    employee = accrual.employee
    if request.method == 'POST':
        form = VacationAccrualForm(request.POST, instance=accrual, employee=employee)
        if form.is_valid():
            form.save()
            return _render_vacation_tab(request, employee)
        return render(request, 'vacations/partials/accrual_edit_modal.html', {'form': form, 'accrual': accrual})
    return HttpResponse(status=405)

def accrual_delete(request, accrual_pk):
    accrual = get_object_or_404(VacationAccrual, pk=accrual_pk)
    employee = accrual.employee
    if request.method == 'POST':
        accrual.delete()
        return _render_vacation_tab(request, employee)
    return HttpResponse(status=405)


# --- Редактирование и удаление Отпусков ---
def vacation_edit_modal(request, vacation_pk):
    vacation = get_object_or_404(Vacation, pk=vacation_pk)
    form = VacationForm(instance=vacation)
    return render(request, 'vacations/partials/vacation_edit_modal.html', {'form': form, 'vacation': vacation})

def vacation_edit_submit(request, vacation_pk):
    vacation = get_object_or_404(Vacation, pk=vacation_pk)
    employee = vacation.employee
    if request.method == 'POST':
        form = VacationForm(request.POST, instance=vacation)
        if form.is_valid():
            form.save()
            return _render_vacation_tab(request, employee)
        return render(request, 'vacations/partials/vacation_edit_modal.html', {'form': form, 'vacation': vacation})
    return HttpResponse(status=405)

def vacation_delete(request, vacation_pk):
    vacation = get_object_or_404(Vacation, pk=vacation_pk)
    employee = vacation.employee
    if request.method == 'POST':
        vacation.delete()
        return _render_vacation_tab(request, employee)
    return HttpResponse(status=405)