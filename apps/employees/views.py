from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from .models import Employee, Child
from .forms import ChildForm
from apps.vacations.services import get_vacation_summary

from apps.directories.models import Department

import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from django.http import HttpResponse
from .forms import ChildForm, ChildEditForm

def employee_list(request):
    """Список сотрудников с расширенным поиском и фильтрами"""
    query = request.GET.get('q', '')
    dept_id = request.GET.get('department', '')
    status = request.GET.get('status', 'active') # По умолчанию - только работающие

    # Базовый запрос
    employees = Employee.objects.select_related('department', 'position')

    # Фильтр по статусу (работает / уволен / все)
    if status == 'active':
        employees = employees.filter(is_active=True)
    elif status == 'fired':
        employees = employees.filter(is_active=False)
    # Если status == 'all', то не фильтруем (показываем всех)

    # Фильтр по подразделению
    if dept_id:
        employees = employees.filter(department_id=dept_id)

    # Поиск по тексту
    if query:
        employees = employees.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(inn__icontains=query)
        )

    # Получаем список подразделений для выпадающего списка
    departments = Department.objects.filter(is_active=True)

    context = {
        'employees': employees,
        'query': query,
        'departments': departments,
        'current_status': status,
        'current_dept': dept_id,
    }
    return render(request, 'employees/list.html', context)


def employee_detail(request, pk):
    """Детальная страница (карточка) сотрудника"""
    employee = get_object_or_404(Employee, pk=pk)

    # Получаем связанные данные
    children = employee.children.all()
    contracts = employee.contracts.all().order_by('-start_date')
    vacations = employee.vacations.all().order_by('-start_date')
    events = employee.hr_events.all().order_by('-event_date')

    context = {
        'employee': employee,
        'children': children,
        'contracts': contracts,
        'vacations': vacations,
        'events': events,
        'vacation_summary': get_vacation_summary(employee), # Здесь работает наш импорт
    }
    return render(request, 'employees/detail.html', context)


def child_add_modal(request, employee_pk):
    """Возвращает HTML-код модального окна с формой"""
    employee = get_object_or_404(Employee, pk=employee_pk)
    form = ChildForm()
    return render(request, 'employees/partials/child_modal.html', {'form': form, 'employee': employee})


def child_add_submit(request, employee_pk):
    """Обрабатывает отправку формы и возвращает обновленный список детей"""
    employee = get_object_or_404(Employee, pk=employee_pk)
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.employee = employee
            child.save()

            # Если успешно - возвращаем обновленный список детей и скрипт для закрытия модалки
            children = employee.children.all()
            response = render(request, 'employees/partials/children_table.html',
                              {'children': children, 'employee': employee})
            # HTMX-триггер для закрытия модального окна
            response['HX-Trigger'] = 'closeModal'
            return response

        # Если есть ошибки - возвращаем форму с ошибками
        return render(request, 'employees/partials/child_modal.html', {'form': form, 'employee': employee})

    return HttpResponse(status=405)

def export_employees_excel(request):
    """Экспорт списка сотрудников в Excel"""
    # Получаем параметры фильтрации из URL (если пользователь нажимал фильтры)
    query = request.GET.get('q', '')
    dept_id = request.GET.get('department', '')
    status = request.GET.get('status', 'active')

    employees = Employee.objects.select_related('department', 'position').order_by('last_name')

    if status == 'active':
        employees = employees.filter(is_active=True)
    elif status == 'fired':
        employees = employees.filter(is_active=False)
    if dept_id:
        employees = employees.filter(department_id=dept_id)
    if query:
        employees = employees.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(inn__icontains=query)
        )

    # Создаем книгу Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Сотрудники"

    # Стили для заголовков
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="343A40", end_color="343A40", fill_type="solid")
    alignment = Alignment(horizontal="center", vertical="center")

    # Заголовки таблицы
    headers = ['ФИО', 'Подразделение', 'Должность', 'Дата приема', 'Телефон', 'ИН', 'Статус']
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = alignment

    # Заполняем данные
    for row_num, emp in enumerate(employees, 2):
        ws.cell(row=row_num, column=1, value=f"{emp.last_name} {emp.first_name} {emp.middle_name}")
        ws.cell(row=row_num, column=2, value=emp.department.name)
        ws.cell(row=row_num, column=3, value=emp.position.name)
        ws.cell(row=row_num, column=4, value=emp.hire_date.strftime('%d.%m.%Y') if emp.hire_date else '')
        ws.cell(row=row_num, column=5, value=emp.phone)
        ws.cell(row=row_num, column=6, value=emp.inn)
        ws.cell(row=row_num, column=7, value="Работает" if emp.is_active else "Уволен")

    # Автоматическая ширина колонок
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    # Готовим ответ
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="employees_export.xlsx"'
    wb.save(response)
    return response


def child_edit_modal(request, child_pk):
    """Возвращает модальное окно для редактирования ребенка"""
    child = get_object_or_404(Child, pk=child_pk)
    form = ChildEditForm(instance=child)
    return render(request, 'employees/partials/child_edit_modal.html', {'form': form, 'child': child})


def child_edit_submit(request, child_pk):
    """Обрабатывает редактирование ребенка"""
    child = get_object_or_404(Child, pk=child_pk)
    employee = child.employee

    if request.method == 'POST':
        form = ChildEditForm(request.POST, instance=child)
        if form.is_valid():
            form.save()
            children = employee.children.all()
            response = render(request, 'employees/partials/children_table.html',
                              {'children': children, 'employee': employee})
            response['HX-Trigger'] = 'closeModal'
            return response
        return render(request, 'employees/partials/child_edit_modal.html', {'form': form, 'child': child})
    return HttpResponse(status=405)


def child_delete(request, child_pk):
    """Удаляет ребенка"""
    child = get_object_or_404(Child, pk=child_pk)
    employee = child.employee
    if request.method == 'POST':
        child.delete()
        children = employee.children.all()
        return render(request, 'employees/partials/children_table.html', {'children': children, 'employee': employee})
    return HttpResponse(status=405)