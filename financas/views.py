from datetime import date
from calendar import monthrange

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from .models import Transacao, Conta
from .forms import TransacaoForm, ContaForm

def _mes_intervalo(yyyy_mm: str | None):
    """Retorna (inicio, fim) do mês. yyyy_mm='2025-09' ou None para mês atual."""
    if yyyy_mm:
        ano, mes = map(int, yyyy_mm.split('-'))
    else:
        hoje = date.today()
        ano, mes = hoje.year, hoje.month
    inicio = date(ano, mes, 1)
    fim = date(ano, mes, monthrange(ano, mes)[1])
    return (inicio, fim), f"{ano:04d}-{mes:02d}"

@login_required
def transacao_list(request):
    # filtro por mês (YYYY-MM) e categoria (opcional)
    (ini, fim), mes_str = _mes_intervalo(request.GET.get('mes'))
    categoria = request.GET.get('cat') or ''

    qs = Transacao.objects.filter(owner=request.user, data__range=(ini, fim))
    if categoria:
        qs = qs.filter(categoria=categoria)
    itens = qs.order_by('-data', '-criado_em')

    # totais
    entradas_total = qs.filter(tipo='E').aggregate(v=Sum('valor'))['v'] or 0
    saidas_total = qs.filter(tipo='S').aggregate(v=Sum('valor'))['v'] or 0
    saidas_pendentes_total = qs.filter(tipo='S', status='pendente').aggregate(v=Sum('valor'))['v'] or 0

    # conta (saldo atual + saldo projetado apos débitos pendentes)
    conta, _ = Conta.objects.get_or_create(owner=request.user, defaults={'saldo_atual': 0})
    saldo_em_conta = conta.saldo_atual or 0
    saldo_pos_debitos = (saldo_em_conta or 0) - (saidas_pendentes_total or 0)

    contexto = {
        'itens': itens,
        'mes': mes_str,
        'categoria_sel': categoria,
        'entradas_total': entradas_total,
        'saidas_total': saidas_total,
        'saidas_pendentes_total': saidas_pendentes_total,
        'saldo_em_conta': saldo_em_conta,
        'saldo_pos_debitos': saldo_pos_debitos,
    }
    return render(request, 'financas/lista.html', contexto)

@login_required
def transacao_create(request):
    form = TransacaoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.owner = request.user
        obj.save()
        messages.success(request, 'Transação criada!')
        return redirect('financas:lista')
    return render(request, 'financas/form.html', {'form': form, 'titulo': 'Nova transação'})

@login_required
def transacao_update(request, pk):
    obj = get_object_or_404(Transacao, pk=pk, owner=request.user)
    form = TransacaoForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Transação atualizada!')
        return redirect('financas:lista')
    return render(request, 'financas/form.html', {'form': form, 'titulo': 'Editar transação'})

@login_required
def transacao_delete(request, pk):
    obj = get_object_or_404(Transacao, pk=pk, owner=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Transação excluída!')
        return redirect('financas:lista')
    return render(request, 'financas/confirm_delete.html', {'obj': obj})

@login_required
def conta_edit(request):
    conta, _ = Conta.objects.get_or_create(owner=request.user, defaults={'saldo_atual': 0})
    form = ContaForm(request.POST or None, instance=conta)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Saldo atualizado!')
        return redirect('financas:lista')
    return render(request, 'financas/conta.html', {'form': form})
