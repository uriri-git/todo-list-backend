from datetime import date
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.enums import PrioridadeTarefa, StatusTarefa
from app.models import Task, User
from app.schemas import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tarefas"])

def owned_task(task_id: int, user: User, db: Session) -> Task:
    task = db.scalar(select(Task).where(Task.id == task_id, Task.owner_id == user.id))
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    return task

@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = Task(**data.model_dump(), owner_id=user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/", response_model=list[TaskOut])
def list_tasks(
    # O parâmetro se chama status_tarefa porque "status" já é o módulo do FastAPI importado acima;
    # o alias mantém o nome público "status" na URL.
    status_tarefa: Annotated[StatusTarefa | None, Query(alias="status")] = None,
    prioridade: Annotated[PrioridadeTarefa | None, Query()] = None,
    prazo_ate: Annotated[date | None, Query(alias="prazoAte", description="Somente tarefas com prazo até esta data")] = None,
    busca: Annotated[str | None, Query(max_length=200, description="Texto contido no título (sem diferenciar maiúsculas)")] = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Lista as tarefas do usuário logado, com filtros opcionais que se combinam.

    Nenhum resultado é uma lista vazia, não um 404.
    """
    query = select(Task).where(Task.owner_id == user.id)
    if status_tarefa is not None:
        query = query.where(Task.completed == (status_tarefa is StatusTarefa.CONCLUIDA))
    if prioridade is not None:
        query = query.where(Task.prioridade == prioridade.value)
    if prazo_ate is not None:
        query = query.where(Task.prazo.is_not(None), Task.prazo <= prazo_ate)
    busca = (busca or "").strip() or None
    if busca:
        # icontains = "contém", sem diferenciar maiúsculas. autoescape faz % e _ serem
        # procurados como texto comum, e não como curingas do LIKE.
        query = query.where(Task.title.icontains(busca, autoescape=True))
    return db.scalars(query.order_by(Task.id)).all()

@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return owned_task(task_id, user, db)

@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Atualiza parcialmente uma tarefa.

    Quando o status muda (por "status" ou por "completed"), a data de conclusão
    é ajustada pela própria tarefa, conforme a RN-03. Se os dois vierem juntos,
    vale o "status".
    """
    task = owned_task(task_id, user, db)
    changes = data.model_dump(exclude_unset=True)
    new_status = changes.pop("status", None)
    completed = changes.pop("completed", None)
    for field, value in changes.items():
        setattr(task, field, value)
    if new_status is not None:
        task.definir_status(new_status)
    elif completed is not None:
        task.definir_status(StatusTarefa.CONCLUIDA if completed else StatusTarefa.PENDENTE)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = owned_task(task_id, user, db)
    db.delete(task)
    db.commit()
