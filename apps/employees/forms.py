from django import forms
from .models import Child

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['full_name', 'birth_date']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов Иван Иванович'}),
            'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget.format = '%Y-%m-%d'

class ChildEditForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['full_name', 'birth_date']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget.format = '%Y-%m-%d'