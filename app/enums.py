"""Valores permitidos de status e prioridade, definidos num lugar só.

Os enums herdam de str: cada valor se comporta como o próprio texto, então
pode ser gravado no banco e enviado no JSON sem conversão.
"""
from enum import Enum


class StatusTarefa(str, Enum):
    PENDENTE = "pendente"
    CONCLUIDA = "concluida"


class PrioridadeTarefa(str, Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"

    @property
    def peso(self) -> int:
        """Peso da prioridade: 0 é a mais urgente. Serve para ordenar na ordem certa."""
        return _PESOS[self]

    @classmethod
    def mapa_de_pesos(cls) -> dict[str, int]:
        """Devolve {"urgente": 0, "alta": 1, ...}, usado para ordenar por prioridade no banco."""
        return {p.value: p.peso for p in cls}


# Fica depois da classe porque usa os membros dela, que só existem depois que ela é criada.
_PESOS = {
    PrioridadeTarefa.URGENTE: 0,
    PrioridadeTarefa.ALTA: 1,
    PrioridadeTarefa.MEDIA: 2,
    PrioridadeTarefa.BAIXA: 3,
}
