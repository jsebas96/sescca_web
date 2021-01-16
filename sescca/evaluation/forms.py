from django import forms
from .models import AutoEvaluation

class AutoEvaluationForm(forms.ModelForm):
    class Meta:
        model = AutoEvaluation
        fields = ("time_range", "activate")

        widgets = {
            'time_range':forms.NumberInput(attrs={'class':'form-control mb-3'})
        }