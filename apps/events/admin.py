from django.contrib import admin
from .models import HREvent, ChangeLog

@admin.register(HREvent)
class HREventAdmin(admin.ModelAdmin):
    list_display = ('employee', 'event_type', 'event_date', 'document_number')
    list_filter = ('event_type', 'event_date')
    search_fields = ('employee__last_name', 'document_number', 'description')
    autocomplete_fields = ['employee']
    date_hierarchy = 'event_date'

@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    list_display = ('changed_at', 'model_name', 'object_id', 'field_name', 'changed_by')
    list_filter = ('model_name', 'changed_by')
    search_fields = ('model_name', 'field_name', 'old_value', 'new_value')
    readonly_fields = (
        'model_name', 'object_id', 'field_name', 'old_value',
        'new_value', 'changed_by', 'changed_at'
    )

    # Запрещаем добавлять и удалять записи вручную
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False