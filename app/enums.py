"""Valores permitidos de status e prioridade, definidos num lugar só.

Os enums herdam de str: cada valor se comporta como o próprio texto, então
pode ser gravado no banco e enviado no JSON sem conversão.
"""
from enum import Enum


class StatusTarefa(str, Enum):
    PENDENTE = "pendente"
    CONCLUIDA = "concluida"
