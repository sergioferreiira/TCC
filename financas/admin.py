from django.contrib import admin
from .models import Transacao, Conta

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'categoria', 'valor', 'data', 'status', 'owner', 'criado_em')
    list_filter = ('tipo', 'categoria', 'status', 'data')
    search_fields = ('titulo', 'obs')

@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('owner', 'saldo_atual')
    search_fields = ('owner__username', 'owner__email')
