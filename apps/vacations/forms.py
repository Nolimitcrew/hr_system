from django import forms
from .models import VacationAccrual, Vacation

class VacationAccrualForm(forms.ModelForm):
    class Meta:
        model = VacationAccrual
        fields = ['work_year', 'days', 'reason', 'date_accrued']
        widgets = {
            'work_year': forms.Select(attrs={'class': 'form-select'}),
            'days': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Основной отпуск'}),
            'date_accrued': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        # Передаем сотрудника, чтобы отфильтровать его рабочие годы
        employee = kwargs.pop('employee', None)
        super().__init__(*args, **kwargs)
        if employee:
            self.fields['work_year'].queryset = employee.work_years.all()

class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = ['vacation_type', 'start_date', 'end_date', 'days', 'status', 'document_number']
        widgets = {
            'vacation_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'days': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'document_number': forms.TextInput(attrs={'class': 'form-control'}),
        }