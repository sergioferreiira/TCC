from django import forms
from .models import Transacao, Conta, Recorrencia

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

class RecorrenciaForm(forms.ModelForm):
    class Meta:
        model = Recorrencia
        fields = ['titulo', 'tipo', 'categoria', 'valor', 'dia_vencimento', 'inicio', 'meses', 'ativo']
        widgets = {
            'inicio': forms.DateInput(attrs={'type': 'date'}),
            'valor': forms.NumberInput(attrs={'step': '0.01'}),
            'dia_vencimento': forms.NumberInput(attrs={'min': 1, 'max': 31}),
            'meses': forms.NumberInput(attrs={'min': 0}),
        }
