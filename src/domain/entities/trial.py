from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .kata import Kata
from .measurement import Measurement
from .treatment import Treatment

COLUNAS = (
	"participante",
	"ordem",
	"kata_id",
	"kata_nome",
	"tratamento",
	"inicio",
	"tempo_segundos",
	"censurado",
	"testes_total",
	"testes_passando",
	"arquivo_solucao",
	"observacoes",
)


@dataclass(frozen=True)
class Trial:
	"""Uma medicao do experimento: um integrante resolvendo um kata sob um tratamento."""

	participante: str
	ordem: int
	kata: Kata
	tratamento: Treatment
	inicio: datetime
	medicao: Measurement
	arquivo_solucao: str
	observacoes: str = ""

	def to_row(self) -> dict[str, str]:
		"""Vira uma linha do trials.csv. A taxa de sucesso fica de fora de proposito:
		e derivada de testes_passando/testes_total e nao deve ser guardada duplicada."""
		return {
			"participante": self.participante,
			"ordem": str(self.ordem),
			"kata_id": self.kata.id,
			"kata_nome": self.kata.nome,
			"tratamento": self.tratamento.value,
			"inicio": self.inicio.isoformat(timespec="seconds"),
			"tempo_segundos": f"{self.medicao.tempo_segundos:.1f}",
			"censurado": "true" if self.medicao.censurado else "false",
			"testes_total": str(self.medicao.testes_total),
			"testes_passando": str(self.medicao.testes_passando),
			"arquivo_solucao": self.arquivo_solucao,
			"observacoes": self.observacoes.replace("\n", " ").strip(),
		}
