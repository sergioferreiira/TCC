from django.db import models
from django.utils import timezone
from django.conf import settings
from decimal import Decimal


class Conta(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conta"
    )
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

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recorrencias"
    )
    titulo = models.CharField(max_length=120)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default="S")
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default="fixa")
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    dia_vencimento = models.PositiveSmallIntegerField(help_text="Dia do mês (1–31)")
    inicio = models.DateField(default=timezone.now, help_text="Mês/ano de início")
    meses = models.PositiveSmallIntegerField(help_text="Duração em meses", default=0)
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
            self.status = "pago"
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
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transacoes",
        null=True,
        blank=True,
    )
    recorrencia = models.ForeignKey(
        Recorrencia,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transacoes",
    )

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


class CotacaoCripto(models.Model):
    """
    Registro de cotação de criptomoeda obtido via API (CoinMarketCap).
    Guardamos histórico para fins de auditoria e análise.
    """

    # Ex.: "BTC", "ETH"
    simbolo = models.CharField("Símbolo", max_length=10, db_index=True)

    # Ex.: "Bitcoin", "Ethereum" (opcional, mas útil para exibição)
    nome = models.CharField("Nome", max_length=50, blank=True, default="")

    # Moeda fiduciária usada na conversão: "USD" ou "BRL"
    moeda_fiat = models.CharField("Moeda Fiat", max_length=5, default="USD")

    # Preço convertido
    preco = models.DecimalField("Preço", max_digits=20, decimal_places=8)

    # Variação percentual nas últimas 24h (ex.: -3.25, 1.02)
    variacao_24h = models.DecimalField(
        "Variação 24h (%)",
        max_digits=7,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    # Momento em que consultamos a API
    data_consulta = models.DateTimeField(
        "Data da consulta", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Cotação de Cripto"
        verbose_name_plural = "Cotações de Cripto"
        ordering = ["-data_consulta", "simbolo"]

    def __str__(self) -> str:
        return f"{self.simbolo} {self.preco} {self.moeda_fiat} @ {self.data_consulta:%Y-%m-%d %H:%M:%S}"
