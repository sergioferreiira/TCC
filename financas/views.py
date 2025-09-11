from datetime import date
from calendar import monthrange
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Transacao, Conta, Recorrencia
from .forms import TransacaoForm, ContaForm, RecorrenciaForm

def _mes_intervalo(yyyy_mm: str | None):
    if yyyy_mm:
        ano, mes = map(int, yyyy_mm.split("-"))
    else:
        hoje = date.today()
        ano, mes = hoje.year, hoje.month
    inicio = date(ano, mes, 1)
    fim = date(ano, mes, monthrange(ano, mes)[1])
    return (inicio, fim), f"{ano:04d}-{mes:02d}"


def _gerar_recorrencias_mes(owner, ano: int, mes: int) -> int:
    criadas = 0
    recs = Recorrencia.objects.filter(owner=owner, ativo=True)
    last_day = monthrange(ano, mes)[1]
    for r in recs:
        if not r.ativa_no_mes(ano, mes):
            continue
        exists = Transacao.objects.filter(owner=owner, recorrencia=r, data__year=ano, data__month=mes).exists()
        if exists:
            continue
        dia = min(r.dia_vencimento, last_day)
        Transacao.objects.create(
            owner=owner,
            recorrencia=r,
            titulo=r.titulo,
            tipo="E" if r.categoria == "salario" else r.tipo,
            categoria=r.categoria,
            valor=r.valor,
            data=date(ano, mes, dia),
            status="pago" if r.categoria == "salario" else "pendente",
            obs="(gerado automaticamente pela recorrência)",
        )
        criadas += 1
    return criadas


@login_required
def transacao_list(request):
    (ini, fim), mes_str = _mes_intervalo(request.GET.get("mes"))
    ano, mes = map(int, mes_str.split("-"))
    categoria = request.GET.get("cat") or ""

    _gerar_recorrencias_mes(request.user, ano, mes)

    qs = Transacao.objects.filter(owner=request.user, data__range=(ini, fim))
    if categoria:
        qs = qs.filter(categoria=categoria)
    itens = qs.order_by("-data", "-criado_em")

    entradas_mes_pagas = qs.filter(tipo="E", status="pago").aggregate(v=Sum("valor"))["v"] or Decimal("0")
    saidas_mes_pagas = qs.filter(tipo="S", status="pago").aggregate(v=Sum("valor"))["v"] or Decimal("0")
    pendentes_mes_total = qs.filter(status="pendente").aggregate(v=Sum("valor"))["v"] or Decimal("0")

    entradas_hist = Transacao.objects.filter(owner=request.user, status="pago", tipo="E", data__lte=fim).aggregate(v=Sum("valor"))["v"] or Decimal("0")
    saidas_hist = Transacao.objects.filter(owner=request.user, status="pago", tipo="S", data__lte=fim).aggregate(v=Sum("valor"))["v"] or Decimal("0")
    saldo_real = entradas_hist - saidas_hist

    saldo_comprometido = saldo_real - pendentes_mes_total

    contexto = {
        "itens": itens,
        "mes": mes_str,
        "categoria_sel": categoria,
        "entradas_mes_pagas": entradas_mes_pagas,
        "saidas_mes_pagas": saidas_mes_pagas,
        "pendentes_mes_total": pendentes_mes_total,
        "saldo_real": saldo_real,
        "saldo_comprometido": saldo_comprometido,
    }
    return render(request, "financas/lista.html", contexto)


@login_required
def transacao_create(request):
    form = TransacaoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.owner = request.user
        obj.save()
        messages.success(request, "Transação criada!")
        return redirect("financas:lista")
    return render(request, "financas/form.html", {"form": form, "titulo": "Nova transação"})


@login_required
def transacao_update(request, pk):
    obj = get_object_or_404(Transacao, pk=pk, owner=request.user)
    form = TransacaoForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Transação atualizada!")
        return redirect("financas:lista")
    return render(request, "financas/form.html", {"form": form, "titulo": "Editar transação"})


@login_required
def transacao_delete(request, pk):
    obj = get_object_or_404(Transacao, pk=pk, owner=request.user)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Transação excluída!")
        return redirect("financas:lista")
    return render(request, "financas/confirm_delete.html", {"obj": obj})


@login_required
def conta_edit(request):
    conta, _ = Conta.objects.get_or_create(owner=request.user, defaults={"saldo_atual": 0})
    form = ContaForm(request.POST or None, instance=conta)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Saldo atualizado!")
        return redirect("financas:lista")
    return render(request, "financas/conta.html", {"form": form})


@login_required
def transacao_create(request):
    form = TransacaoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.owner = request.user
        obj.save()  # salva o mês atual

        # Se categoria variável e houver meses adicionais, cria cópias futuras como PENDENTES
        if obj.categoria == "variavel":
            repetir = form.cleaned_data.get("repetir_meses") or 0
            if repetir > 0:
                y, m, d = obj.data.year, obj.data.month, obj.data.day
                for i in range(1, repetir + 1):
                    # avança i meses
                    new_m = m + i
                    new_y = y + (new_m - 1) // 12
                    new_m = ((new_m - 1) % 12) + 1
                    last_day = monthrange(new_y, new_m)[1]
                    new_d = min(d, last_day)

                    Transacao.objects.create(
                        owner=request.user,
                        recorrencia=obj.recorrencia,  # normalmente None
                        titulo=obj.titulo,
                        tipo=obj.tipo,                 # mantém E/S
                        categoria=obj.categoria,       # variavel
                        valor=obj.valor,
                        data=date(new_y, new_m, new_d),
                        status="pendente",             # futuras sempre pendentes
                        obs=f"(gerado automaticamente - {i}º mês)",
                    )

        messages.success(request, "Transação criada!")
        return redirect("financas:lista")
    return render(request, "financas/form.html", {"form": form, "titulo": "Nova transação"})