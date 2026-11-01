from django.contrib import admin
from .models import TelegramNotification, ActionLog


@admin.register(TelegramNotification)
class TelegramNotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient_chat_id', 'status', 'created_at', 'sent_at')
    list_filter = ('status',)
    readonly_fields = ('created_at', 'sent_at')


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action')
    list_filter = ('user', 'timestamp')
    readonly_fields = ('user', 'action', 'details', 'timestamp')

    # Запрещаем редактировать и удалять логи
    def has_add_permission(self, request): return False

    def has_delete_permission(self, request, obj=None): return False