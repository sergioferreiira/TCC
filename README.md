# 💼 TCC — Sistema de Finanças (Django)

Projeto de controle financeiro pessoal com **transações**, **conta**, **recorrências** e módulo opcional de **cotações de criptomoedas** (CoinMarketCap).

---

## 🔎 Visão Geral

- Cadastro e gestão de **transações** (entradas/saídas, status e categorias).
- **Geração automática** de transações a partir de **recorrências** (ex.: salário).
- Cálculos de **saldo real** e **saldo comprometido**.
- **Filtros** por mês e categoria + **dashboard** com métricas.
- **Módulo Criptos**: consulta preços em tempo real, salva histórico e exibe no front.

---

## 🧱 Tecnologias

- **Python / Django**
- **Bootstrap** (templates)
- **SQLite/PostgreSQL** (Django ORM)
- **Requests** (integração HTTP)
- (Opcional) **CoinMarketCap API**

---

## 🚀 Como rodar

```bash
# 1) Crie e ative o venv
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 2) Instale dependências
pip install -r requirements.txt

# 3) Migre o banco
python manage.py migrate

# 4) Crie superusuário
python manage.py createsuperuser

# 5) Rode o servidor
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000/`

---

## 📦 Estrutura

```
TCC/
├─ config/
│  └─ (settings/urls/etc.)
├─ financas/
│  ├─ api/
│  │  ├─ __init__.py
│  │  └─ coinmarketcap.py
│  ├─ migrations/
│  ├─ static/
│  │  └─ js/
│  │     └─ criptos.js
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ models.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ templates/
│  └─ financas/
│     ├─ base.html
│     ├─ lista.html
│     ├─ form.html
│     ├─ conta.html
│     ├─ confirm_delete.html
│     └─ criptos.html
│  └─ registration/
│     └─ login.html
├─ venv/
```

---

## 🪙 Módulo Opcional: Criptomoedas

- **O que faz:** consulta **BTC/ETH** (ou outros símbolos) em tempo real, **salva no banco** e exibe.
- **Endpoint interno:** `/criptos/atualizar/?symbols=BTC,ETH&convert=USD`
- **Página dedicada:** `/criptos/` (com botão **Checar Criptos** + histórico)
- **API Key** no servidor:
  ```python
  # settings.py
  COINMARKETCAP_API_KEY = os.environ.get("CMC_API_KEY", "")
  ```
  ```powershell
  # Windows PowerShell
  $env:CMC_API_KEY="SUA_CHAVE_AQUI"
  ```

---

## 🧭 Uso

- Dashboard: filtrar por **mês** e **categoria**; criar/editar/excluir transações.
- Recorrências: o sistema **gera automaticamente** lançamentos do mês.
- Criptos: acessar `/criptos/` ou usar o **botão do dashboard** (consulta rápida).

---

## ✅ Teste rápido

- **JSON:** `http://127.0.0.1:8000/criptos/atualizar/?symbols=BTC,ETH&convert=USD`
- **Página:** `http://127.0.0.1:8000/criptos/`

> Necessário usuário autenticado.

---

## 📄 Licença

Projeto acadêmico (TCC). Uso educacional.
