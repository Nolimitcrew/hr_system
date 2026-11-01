from django.contrib import admin
from django.urls import path, include

# Импорты наших представлений
from apps.accounts.views import home
from apps.employees.views import (
    employee_list,
    employee_detail,
    child_add_modal,
    child_add_submit,
    export_employees_excel
)
from apps.contracts.views import (
    contract_add_modal,
    contract_add_submit
)
from apps.vacations.views import (
    accrual_add_modal,
    accrual_add_submit,
    vacation_add_modal,
    vacation_add_submit,
    vacation_global_list
)
from apps.events.views import event_global_list
from apps.directories.views import (
    directories_list,
    dept_add_modal, dept_add_submit,
    pos_add_modal, pos_add_submit,
    prof_add_modal, prof_add_submit
)
from apps.accounts.views import home, user_list, user_add_modal, user_add_submit

urlpatterns = [
    # Админка Django
    path('admin/', admin.site.urls),

    # Авторизация (вход/выход)
    path('accounts/', include('django.contrib.auth.urls')),

    # Главная страница
    path('', home, name='home'),

    # --- Сотрудники ---
    path('employees/', employee_list, name='employee_list'),
    path('employees/export/', export_employees_excel, name='export_employees'),
    path('employees/<int:pk>/', employee_detail, name='employee_detail'),

    # --- Дети (HTMX) ---
    path('employees/<int:employee_pk>/child/modal/', child_add_modal, name='child_add_modal'),
    path('employees/<int:employee_pk>/child/add/', child_add_submit, name='child_add_submit'),

    # --- Контракты (HTMX) ---
    path('employees/<int:employee_pk>/contract/modal/', contract_add_modal, name='contract_add_modal'),
    path('employees/<int:employee_pk>/contract/add/', contract_add_submit, name='contract_add_submit'),

    # --- Начисления (HTMX) ---
    path('employees/<int:employee_pk>/accrual/modal/', accrual_add_modal, name='accrual_add_modal'),
    path('employees/<int:employee_pk>/accrual/add/', accrual_add_submit, name='accrual_add_submit'),

    # --- Отпуска (HTMX) ---
    path('employees/<int:employee_pk>/vacation/modal/', vacation_add_modal, name='vacation_add_modal'),
    path('employees/<int:employee_pk>/vacation/add/', vacation_add_submit, name='vacation_add_submit'),

    # --- Глобальные реестры ---
    path('vacations/', vacation_global_list, name='vacation_global_list'),
    path('events/', event_global_list, name='event_global_list'),


    path('directories/', directories_list, name='directories_list'),
    path('directories/dept/modal/', dept_add_modal, name='dept_add_modal'),
    path('directories/dept/add/', dept_add_submit, name='dept_add_submit'),
    path('directories/pos/modal/', pos_add_modal, name='pos_add_modal'),
    path('directories/pos/add/', pos_add_submit, name='pos_add_submit'),
    path('directories/prof/modal/', prof_add_modal, name='prof_add_modal'),
    path('directories/prof/add/', prof_add_submit, name='prof_add_submit'),
    path('users/', user_list, name='user_list'),
    path('users/modal/', user_add_modal, name='user_add_modal'),
    path('users/add/', user_add_submit, name='user_add_submit'),

]