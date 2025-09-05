from django.db import models
from django.utils import timezone
from django.conf import settings

class Conta(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conta')
    saldo_atual = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Conta de {self.owner} — Saldo: R$ {self.saldo_atual}"

class Transacao(models.Model):
    TIPO_CHOICES = (
        ('E', 'Entrada'),
        ('S', 'Saída'),
    )
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
    )
    CATEGORIAS = (
        ('fixa', 'Fixa'),
        ('variavel', 'Variável'),
        ('lazer', 'Lazer'),
        ('alimentacao', 'Alimentação'),
        ('outros', 'Outros'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transacoes', null=True, blank=True)
    titulo = models.CharField(max_length=120)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='outros')
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    obs = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()}) - R$ {self.valor}"
