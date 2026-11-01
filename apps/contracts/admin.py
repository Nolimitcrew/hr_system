# apps/contracts/admin.py
from django.contrib import admin
from .models import Contract, WorkYear

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'employee', 'contract_type', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'contract_type')
    search_fields = ('contract_number', 'employee__last_name')
    autocomplete_fields = ['employee']

@admin.register(WorkYear)
class WorkYearAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'is_closed')
    list_filter = ('is_closed',)
    search_fields = ('employee__last_name',)
    autocomplete_fields = ['employee']