from django.contrib import admin
from .models import (
    Conta,
    Transacao,
    Recorrencia,
    CotacaoCripto,
    MetaFinanceira,
    ChatMessage,
)


@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ("owner", "saldo_atual")
    search_fields = ("owner__username", "owner__email")


@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "owner",
        "categoria",
        "tipo",
        "valor",
        "status",
        "data",
        "criado_em",
    )
    list_filter = ("categoria", "tipo", "status", "data")
    search_fields = ("titulo", "owner__username", "owner__email")
    ordering = ("-data", "-criado_em")

    def save_model(self, request, obj, form, change):
        if obj.categoria == "salario":
            obj.tipo = "E"
            obj.status = "pago"
        super().save_model(request, obj, form, change)


@admin.register(Recorrencia)
class RecorrenciaAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "owner",
        "categoria",
        "tipo",
        "valor",
        "dia_vencimento",
        "ativo",
        "inicio",
        "meses",
    )
    list_filter = ("categoria", "tipo", "ativo")
    search_fields = ("titulo", "owner__username", "owner__email")
    ordering = ("-inicio",)

    def save_model(self, request, obj, form, change):
        if obj.categoria == "salario":
            obj.tipo = "E"
        super().save_model(request, obj, form, change)


@admin.register(CotacaoCripto)
class CotacaoCriptoAdmin(admin.ModelAdmin):
    list_display = (
        "data_consulta",
        "simbolo",
        "nome",
        "preco",
        "moeda_fiat",
        "variacao_24h",
    )
    list_filter = ("simbolo", "moeda_fiat", "data_consulta")
    search_fields = ("simbolo", "nome")
    ordering = ("-data_consulta",)


admin.site.register(MetaFinanceira)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("autor", "texto", "criado_em")
    list_filter = ("autor", "criado_em")
    search_fields = ("texto",)
