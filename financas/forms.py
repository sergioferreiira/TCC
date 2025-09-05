from django import forms
from .models import Transacao, Conta

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['titulo', 'tipo', 'categoria', 'valor', 'data', 'status', 'obs']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['saldo_atual']
        widgets = {
            'saldo_atual': forms.NumberInput(attrs={'step': '0.01'}),
        }
