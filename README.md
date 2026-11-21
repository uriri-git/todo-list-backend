# TODO LIST API

API REST de lista de tarefas construída com FastAPI, SQLAlchemy e SQLite.

## Requisitos
- Python 3.13
- Git

## Instalação (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edite `.env` e substitua `JWT_SECRET` por uma chave longa e aleatória.

## Executar

```powershell
uvicorn app.main:app --reload
```

Documentação interativa: http://127.0.0.1:8000/docs

## Rotas
- `POST /auth/register` — criar conta
- `POST /auth/login` — entrar e receber token
- `GET /users/me` — consultar perfil autenticado
- `POST /tasks/` — criar tarefa
- `GET /tasks/` — listar tarefas do usuário
- `GET /tasks/{task_id}` — consultar tarefa
- `PATCH /tasks/{task_id}` — editar tarefa; aceita `status` (`pendente` ou `concluida`) e registra `concluido_em` (RN-03)
- `DELETE /tasks/{task_id}` — excluir tarefa

As rotas de perfil e tarefas exigem `Authorization: Bearer <token>`.
Cada usuário só acessa suas próprias tarefas.

## Observação
Este projeto foi montado como implementação funcional independente a partir dos tópicos informados na conversa. Não é uma transcrição literal dos manuais internos do SENAC.
