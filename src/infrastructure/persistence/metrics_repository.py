from __future__ import annotations

import csv
from pathlib import Path

COLUNAS = (
	"participante",
	"ordem",
	"kata_id",
	"tratamento",
	"arquivo",
	"funcoes",
	"cc_media",
	"cc_max",
	"loc",
	"sloc",
	"comentarios",
	"mi",
	"duplicacao_pct",
	"linhas_duplicadas",
	"observacao",
)


class CsvMetricsRepository:
	"""Grava as metricas estaticas dos 12 trials num CSV unico.

	Diferente dos trials, aqui um arquivo so nao da conflito: as metricas sao geradas
	de uma vez, em lote, depois que todos os trials terminaram.
	"""

	def __init__(self, destino: Path) -> None:
		self._destino = Path(destino)

	def salvar(self, linhas: list[dict[str, str]]) -> Path:
		self._destino.parent.mkdir(parents=True, exist_ok=True)

		with self._destino.open("w", newline="", encoding="utf-8") as arquivo:
			escritor = csv.DictWriter(arquivo, fieldnames=list(COLUNAS))
			escritor.writeheader()
			escritor.writerows(linhas)

		return self._destino
