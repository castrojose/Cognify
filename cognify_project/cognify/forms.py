from django import forms
from .models import Criminal

class CriminalForm(forms.ModelForm):
    class Meta:
        model = Criminal
        fields = ['name', 'crime_type', 'age']  # Asegúrate de incluir 'age' si es necesario
