from django import forms
from .models import Transacao, Conta, Recorrencia

class TransacaoForm(forms.ModelForm):
    repetir_meses = forms.IntegerField(
        min_value=0, required=False, initial=0,
        label="Repetir por (meses adicionais)",
        help_text="Ex.: 2 → cria também nos próximos 2 meses"
    )

    class Meta:
        model = Transacao
        fields = ["titulo", "tipo", "categoria", "valor", "data", "status", "obs"]  
        widgets = {
            "titulo":   forms.TextInput(attrs={"class": "form-control"}),
            "tipo":     forms.Select(attrs={"class": "form-select"}),
            "categoria":forms.Select(attrs={"class": "form-select"}),
            "valor":    forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "data":     forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "status":   forms.Select(attrs={"class": "form-select"}),
            "obs":      forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("categoria") == "salario":
            cleaned["tipo"] = "E"
            cleaned["status"] = "pago"
        if cleaned.get("repetir_meses") is None:
            cleaned["repetir_meses"] = 0
        return cleaned


class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ["saldo_atual"]
        widgets = {"saldo_atual": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"})}


class RecorrenciaForm(forms.ModelForm):
    class Meta:
        model = Recorrencia
        fields = ["titulo", "tipo", "categoria", "valor", "dia_vencimento", "inicio", "meses", "ativo"]
        widgets = {
            "titulo":         forms.TextInput(attrs={"class": "form-control"}),
            "tipo":           forms.Select(attrs={"class": "form-select"}),
            "categoria":      forms.Select(attrs={"class": "form-select"}),
            "valor":          forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "dia_vencimento": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 31}),
            "inicio":         forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "meses":          forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "ativo":          forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("categoria") == "salario":
            cleaned["tipo"] = "E"
        return cleaned
