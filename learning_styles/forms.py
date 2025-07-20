from django import forms
from .models import DiagnosticResponse

class DiagnosticResponseForm(forms.ModelForm):
    class Meta:
        model = DiagnosticResponse
        fields = ['score']
        widgets = {
            'score': forms.RadioSelect(choices=[
                (1, 'Mutlaqo qo\'shilmayman'),
                (2, 'Qo\'shilmayman'),
                (3, 'Neytral'),
                (4, 'Qo\'shilaman'),
                (5, 'To\'liq qo\'shilaman'),
            ])
        }
