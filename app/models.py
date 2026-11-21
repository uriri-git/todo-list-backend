from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.enums import StatusTarefa

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    tasks: Mapped[list["Task"]] = relationship(back_populates="owner", cascade="all, delete-orphan")

    def pending_tasks(self) -> list["Task"]:
        """Tarefas do usuário que ainda não foram concluídas."""
        return [task for task in self.tasks if task.status is StatusTarefa.PENDENTE]

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    concluido_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    owner: Mapped[User] = relationship(back_populates="tasks")

    # ------------------------------------------------------------------ status (RN-03)
    @property
    def status(self) -> StatusTarefa:
        """Status atual, como membro do enum. Somente leitura: para mudar, use concluir/reabrir."""
        return StatusTarefa.CONCLUIDA if self.completed else StatusTarefa.PENDENTE

    def concluir(self, agora: datetime | None = None) -> None:
        """Conclui a tarefa e registra o momento da conclusão (RN-03).

        Se a tarefa já está concluída, não faz nada: é isso que impede que
        mandar "concluída" de novo (ou editar uma tarefa antiga) falsifique
        a data em que ela foi realmente concluída.
        """
        if self.completed:
            return
        self.completed = True
        self.concluido_em = agora or datetime.now(timezone.utc).replace(tzinfo=None)

    def reabrir(self) -> None:
        """Devolve a tarefa para pendente e apaga a data de conclusão (RN-03)."""
        if not self.completed:
            return
        self.completed = False
        self.concluido_em = None

    def definir_status(self, novo_status: StatusTarefa | str, agora: datetime | None = None) -> None:
        """Aplica o status informado pela operação correspondente (concluir ou reabrir)."""
        if StatusTarefa(novo_status) is StatusTarefa.CONCLUIDA:
            self.concluir(agora)
        else:
            self.reabrir()
