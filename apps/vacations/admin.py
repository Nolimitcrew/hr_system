from django.contrib import admin
from .models import VacationAccrual, Vacation

@admin.register(VacationAccrual)
class VacationAccrualAdmin(admin.ModelAdmin):
    list_display = ('employee', 'work_year', 'days', 'reason', 'date_accrued')
    search_fields = ('employee__last_name', 'reason')
    autocomplete_fields = ['employee', 'work_year']

@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'days', 'vacation_type', 'status')
    list_filter = ('status', 'vacation_type')
    search_fields = ('employee__last_name', 'document_number')
    date_hierarchy = 'start_date'
    autocomplete_fields = ['employee']