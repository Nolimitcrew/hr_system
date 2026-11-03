from django.contrib import admin
from .models import Department, Position, Profession

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


from .models import OrganizationSettings # Добавьте в импорты сверху

@admin.register(OrganizationSettings)
class OrganizationSettingsAdmin(admin.ModelAdmin):
    # Указываем путь к нашему кастомному шаблону
    change_form_template = 'admin/directories/organizationsettings/change_form.html'

    def has_add_permission(self, request):
        # Разрешаем создать только одну запись
        if OrganizationSettings.objects.exists():
            return False
        return True