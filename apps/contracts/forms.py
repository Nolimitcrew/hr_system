from django import forms
from .models import Contract

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['contract_number', 'contract_type', 'start_date', 'end_date', 'is_active']
        widgets = {
            'contract_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: 15-к'}),
            'contract_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Принудительно задаем формат для браузера
        self.fields['start_date'].widget.format = '%Y-%m-%d'
        self.fields['end_date'].widget.format = '%Y-%m-%d'