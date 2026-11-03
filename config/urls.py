from django.contrib import admin
from django.urls import path, include

# Импорты наших представлений
from apps.accounts.views import home, user_list, user_add_modal, user_add_submit
from apps.employees.views import (
    employee_list,
    employee_detail,
    child_add_modal,
    child_add_submit,
    child_edit_modal,
    child_edit_submit,
    child_delete,
    export_employees_excel
)
from apps.contracts.views import (
    contract_add_modal,
    contract_add_submit,
    contract_edit_modal,
    contract_edit_submit
)
from apps.directories.views import (
    # ... существующие ...
    settings_view
)
from apps.vacations.views import (
    accrual_add_modal,
    accrual_add_submit,
    accrual_edit_modal,
    accrual_edit_submit,
    accrual_delete,
    vacation_add_modal,
    vacation_add_submit,
    vacation_edit_modal,
    vacation_edit_submit,
    vacation_delete,
    vacation_global_list
)
from apps.events.views import event_global_list
from apps.directories.views import (
    directories_list,
    dept_add_modal, dept_add_submit,
    pos_add_modal, pos_add_submit,
    prof_add_modal, prof_add_submit
)
from apps.notifications.views import telegram_test_modal, telegram_test_submit  # <-- Импорт Telegram

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
    path('child/<int:child_pk>/edit/modal/', child_edit_modal, name='child_edit_modal'),
    path('child/<int:child_pk>/edit/', child_edit_submit, name='child_edit_submit'),
    path('child/<int:child_pk>/delete/', child_delete, name='child_delete'),

    # --- Контракты (HTMX) ---
    path('employees/<int:employee_pk>/contract/modal/', contract_add_modal, name='contract_add_modal'),
    path('employees/<int:employee_pk>/contract/add/', contract_add_submit, name='contract_add_submit'),
    path('contract/<int:contract_pk>/edit/modal/', contract_edit_modal, name='contract_edit_modal'),
    path('contract/<int:contract_pk>/edit/', contract_edit_submit, name='contract_edit_submit'),

    # --- Начисления (HTMX) ---
    path('employees/<int:employee_pk>/accrual/modal/', accrual_add_modal, name='accrual_add_modal'),
    path('employees/<int:employee_pk>/accrual/add/', accrual_add_submit, name='accrual_add_submit'),
    path('accrual/<int:accrual_pk>/edit/modal/', accrual_edit_modal, name='accrual_edit_modal'),
    path('accrual/<int:accrual_pk>/edit/', accrual_edit_submit, name='accrual_edit_submit'),
    path('accrual/<int:accrual_pk>/delete/', accrual_delete, name='accrual_delete'),

    # --- Отпуска (HTMX) ---
    path('employees/<int:employee_pk>/vacation/modal/', vacation_add_modal, name='vacation_add_modal'),
    path('employees/<int:employee_pk>/vacation/add/', vacation_add_submit, name='vacation_add_submit'),
    path('vacation/<int:vacation_pk>/edit/modal/', vacation_edit_modal, name='vacation_edit_modal'),
    path('vacation/<int:vacation_pk>/edit/', vacation_edit_submit, name='vacation_edit_submit'),
    path('vacation/<int:vacation_pk>/delete/', vacation_delete, name='vacation_delete'),

    # --- Глобальные реестры ---
    path('vacations/', vacation_global_list, name='vacation_global_list'),
    path('events/', event_global_list, name='event_global_list'),

    # --- Справочники ---
    path('directories/', directories_list, name='directories_list'),
    path('directories/dept/modal/', dept_add_modal, name='dept_add_modal'),
    path('directories/dept/add/', dept_add_submit, name='dept_add_submit'),
    path('directories/pos/modal/', pos_add_modal, name='pos_add_modal'),
    path('directories/pos/add/', pos_add_submit, name='pos_add_submit'),
    path('directories/prof/modal/', prof_add_modal, name='prof_add_modal'),
    path('directories/prof/add/', prof_add_submit, name='prof_add_submit'),

    path('settings/', settings_view, name='settings_view'),

    # --- Пользователи ---
    path('users/', user_list, name='user_list'),
    path('users/modal/', user_add_modal, name='user_add_modal'),
    path('users/add/', user_add_submit, name='user_add_submit'),

    # --- Уведомления (Telegram) ---
    path('telegram/test/modal/', telegram_test_modal, name='telegram_test_modal'),
    path('telegram/test/submit/', telegram_test_submit, name='telegram_test_submit'),
]