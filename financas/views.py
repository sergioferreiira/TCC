from datetime import date
from calendar import monthrange

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Transacao, Conta, Recorrencia
from .forms import TransacaoForm, ContaForm, RecorrenciaForm

def _mes_intervalo(yyyy_mm: str | None):
    """Retorna ((inicio, fim), 'YYYY-MM')."""
    if yyyy_mm:
        ano, mes = map(int, yyyy_mm.split('-'))
    else:
        hoje = date.today()
        ano, mes = hoje.year, hoje.month
    inicio = date(ano, mes, 1)
    fim = date(ano, mes, monthrange(ano, mes)[1])
    return (inicio, fim), f"{ano:04d}-{mes:02d}"

def _gerar_recorrencias_mes(owner, ano: int, mes: int) -> int:
    """Cria transações faltantes para todas as recorrências ativas do usuário no mês alvo. Retorna quantas foram criadas."""
    criadas = 0
    recs = Recorrencia.objects.filter(owner=owner, ativo=True)
    last_day = monthrange(ano, mes)[1]
    for r in recs:
        if not r.ativa_no_mes(ano, mes):
            continue
        # Já existe transação dessa recorrência neste mês?
        exists = Transacao.objects.filter(owner=owner, recorrencia=r, data__year=ano, data__month=mes).exists()
        if exists:
            continue
        dia = min(r.dia_vencimento, last_day)
        Transacao.objects.create(
            owner=owner,
            recorrencia=r,
            titulo=r.titulo,
            tipo=r.tipo,
            categoria=r.categoria,
            valor=r.valor,
            data=date(ano, mes, dia),
            status='pendente',
            obs='(gerado automaticamente pela recorrência)',
        )
        criadas += 1
    return criadas

@login_required
def transacao_list(request):
    # Filtro por mês e categoria
    (ini, fim), mes_str = _mes_intervalo(request.GET.get('mes'))
    ano, mes = map(int, mes_str.split('-'))
    categoria = request.GET.get('cat') or ''

    # Geração automática de recorrências do mês alvo
    _gerar_recorrencias_mes(request.user, ano, mes)

    qs = Transacao.objects.filter(owner=request.user, data__range=(ini, fim))
    if categoria:
        qs = qs.filter(categoria=categoria)
    itens = qs.order_by('-data', '-criado_em')

    # totais
    entradas_total = qs.filter(tipo='E').aggregate(v=Sum('valor'))['v'] or 0
    saidas_total = qs.filter(tipo='S').aggregate(v=Sum('valor'))['v'] or 0
    saidas_pendentes_total = qs.filter(tipo='S', status='pendente').aggregate(v=Sum('valor'))['v'] or 0

    # conta/saldo
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

# ---- Recorrências (CRUD) ----

@login_required
def recorrencia_list(request):
    itens = Recorrencia.objects.filter(owner=request.user).order_by('-ativo', 'titulo')
    return render(request, 'financas/recorrencia_list.html', {'itens': itens})

@login_required
def recorrencia_create(request):
    form = RecorrenciaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.owner = request.user
        form.save()
        messages.success(request, 'Recorrência criada!')
        return redirect('financas:recorrencias')
    return render(request, 'financas/recorrencia_form.html', {'form': form, 'titulo': 'Nova recorrência'})

@login_required
def recorrencia_update(request, pk):
    obj = get_object_or_404(Recorrencia, pk=pk, owner=request.user)
    form = RecorrenciaForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Recorrência atualizada!')
        return redirect('financas:recorrencias')
    return render(request, 'financas/recorrencia_form.html', {'form': form, 'titulo': 'Editar recorrência'})

@login_required
def recorrencia_toggle(request, pk):
    obj = get_object_or_404(Recorrencia, pk=pk, owner=request.user)
    obj.ativo = not obj.ativo
    obj.save(update_fields=['ativo'])
    messages.success(request, f"Recorrência {'ativada' if obj.ativo else 'desativada'}!")
    return redirect('financas:recorrencias')
