from django.contrib import admin
from .models import Employee, Child


class ChildInline(admin.TabularInline):
    """Позволяет добавлять детей прямо в карточке сотрудника"""
    model = Child
    extra = 1  # Показывать одну пустую строку для добавления


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'position', 'department', 'is_active')
    list_filter = ('is_active', 'department', 'position')
    search_fields = ('last_name', 'first_name', 'middle_name', 'inn', 'phone')

    # Группировка полей в карточке для удобства
    fieldsets = (
        ('Личные данные', {
            'fields': ('last_name', 'first_name', 'middle_name', 'birth_date', 'inn')
        }),
        ('Документы и контакты', {
            'fields': ('passport_series', 'passport_number', 'address', 'phone', 'email')
        }),
        ('Кадровая информация', {
            'fields': ('hire_date', 'dismissal_date', 'is_active', 'department', 'position', 'profession',
                       'default_vacation_days')
        }),
    )

    inlines = [ChildInline]