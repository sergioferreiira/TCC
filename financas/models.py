from django.db import models
from django.utils import timezone
from django.conf import settings


class Conta(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conta")
    saldo_atual = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Conta de {self.owner} — Saldo: R$ {self.saldo_atual}"


class Recorrencia(models.Model):
    TIPO_CHOICES = (("E", "Entrada"), ("S", "Saída"))
    CATEGORIAS = (
        ("salario", "Salário"),
        ("fixa", "Fixa"),
        ("variavel", "Variável"),
        ("lazer", "Lazer"),
        ("alimentacao", "Alimentação"),
        ("outros", "Outros"),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recorrencias")
    titulo = models.CharField(max_length=120)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default="S")
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default="fixa")
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    dia_vencimento = models.PositiveSmallIntegerField(help_text="Dia do mês (1–31)")
    inicio = models.DateField(default=timezone.now, help_text="Mês/ano de início")
    meses = models.PositiveSmallIntegerField(help_text="Duração em meses (ex.: 6). Use 0 para indefinido.", default=0)
    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()}) R$ {self.valor}"

    def ativa_no_mes(self, ano: int, mes: int) -> bool:
        ini_ano, ini_mes = self.inicio.year, self.inicio.month
        idx_ini = ini_ano * 12 + (ini_mes - 1)
        idx_alvo = ano * 12 + (mes - 1)
        if idx_alvo < idx_ini:
            return False
        if self.meses and idx_alvo > (idx_ini + self.meses - 1):
            return False
        return self.ativo

    def save(self, *args, **kwargs):
        if self.categoria == "salario":
            self.tipo = "E"
        super().save(*args, **kwargs)


class Transacao(models.Model):
    TIPO_CHOICES = (("E", "Entrada"), ("S", "Saída"))
    STATUS_CHOICES = (("pendente", "Pendente"), ("pago", "Pago"))
    CATEGORIAS = (
        ("salario", "Salário"),
        ("fixa", "Fixa"),
        ("variavel", "Variável"),
        ("lazer", "Lazer"),
        ("alimentacao", "Alimentação"),
        ("outros", "Outros"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transacoes", null=True, blank=True
    )
    recorrencia = models.ForeignKey(Recorrencia, on_delete=models.SET_NULL, null=True, blank=True, related_name="transacoes")

    titulo = models.CharField(max_length=120)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default="outros")
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pendente")
    obs = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()}) - R$ {self.valor}"

    def save(self, *args, **kwargs):
        if self.categoria == "salario":
            self.tipo = "E"
            self.status = "pago"
        super().save(*args, **kwargs)
