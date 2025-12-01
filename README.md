💼 TCC — Sistema de Finanças Pessoais + Integração com IA (Django + Gemini)

Sistema completo de gestão financeira pessoal, com módulo de análise inteligente via IA, controle de transações, recorrências, metas, saldo, e painel com métricas. Possui ainda um módulo opcional de cotações de criptomoedas com histórico salvo no banco.

📌 Recursos Principais
💰 1. Transações

Entradas e saídas

Categorias, status e datas

Edição e exclusão

Filtro por mês e categoria

🔄 2. Recorrências

Cadastro de despesas/receitas mensais

Geração automática de transações

Controle de ativação por mês

🎯 3. Metas Financeiras

Criação de metas com valor objetivo

Salvo por usuário

🧾 4. Conta

Saldo atual

Integração com transações

📊 5. Dashboard

Gráficos e métricas automáticas:

Total de entradas/saídas

Saldo real

Saldo comprometido

Metas

🤖 6. Chat Inteligente (Gemini IA) — NOVO

Assistente financeiro integrado ao sistema.

O usuário pode:

Tirar dúvidas financeiras

Receber recomendações

Interpretar transações

Analisar despesas, metas e padrões

O chat é restrito exclusivamente ao tema financeiro, por segurança e foco acadêmico.

🪙 7. Módulo de Criptomoedas (Opcional)

Consulta preços (CoinMarketCap API)

Armazena histórico

Exibe gráfico por data

🧠 IA Integrada (Gemini) — Como funciona

O sistema possui uma rota dedicada ao chat:

/gemini/

Fluxo:

O usuário envia uma pergunta.

A view monta um prompt seguro e restrito ao tema financeiro.

O Gemini responde sob regras específicas:

Não sair do tema financeiro.

Não responder assuntos externos.

Respostas claras e didáticas.

A resposta é exibida no front-end imediatamente.

A pergunta e resposta são armazenadas no banco (para avaliação e histórico).

🔒 Prompt usado (versão aprimorada e profissional)
Você é um assistente financeiro integrado a um sistema de gestão pessoal.
Responda somente perguntas diretamente relacionadas a dinheiro, finanças,
orçamento, dívidas, investimentos, contas, criptomoedas, metas, salário,
balanço mensal, planejamento financeiro ou temas correlatos.

Se o usuário perguntar algo fora desse escopo, responda educadamente:
"Sou um assistente financeiro e só posso responder dúvidas sobre finanças."

Sempre mantenha respostas:
- Objetivas
- Técnicas quando necessário
- Simples de entender
- Baseadas apenas na pergunta do usuário e no domínio financeiro

🧱 Tecnologias

Python 3 / Django 4

Gemini API (Google AI)

Bootstrap 5

JavaScript / Fetch API

SQLite ou PostgreSQL

Requests (HTTP / APIs externas)

🛠 Como rodar o projeto
# 1. Criar e ativar venv
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Criar banco
python manage.py migrate

# 4. Criar usuário admin
python manage.py createsuperuser

# 5. Rodar servidor
python manage.py runserver


Acesse:
http://127.0.0.1:8000/

🔑 Configurar Gemini API

No settings.py:

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")


No Windows PowerShell:

$env:GEMINI_API_KEY="SUA_CHAVE_AQUI"

Chat IA
/gemini/

📄 Licença

Projeto acadêmico desenvolvido exclusivamente para fins educacionais.
