from __future__ import annotations

import csv
from pathlib import Path

from ...domain.entities.trial import COLUNAS
from ...infrastructure.persistence.trial_repository import CsvTrialRepository

COLUNAS_EXPORT = (*COLUNAS, "taxa_sucesso", "testes_falhando")


class ExportExperimentData:
	"""Junta os CSVs dos dois participantes num dataset unico para a analise da S03.

	As colunas derivadas (taxa de sucesso e testes falhando) sao calculadas aqui, e nao
	guardadas no bruto, para nao existir a chance de divergirem do dado original.
	"""

	def __init__(self, repositorio: CsvTrialRepository) -> None:
		self._repositorio = repositorio

	def execute(self, destino: Path) -> Path:
		linhas = self._repositorio.read_all()
		destino = Path(destino)
		destino.parent.mkdir(parents=True, exist_ok=True)

		with destino.open("w", newline="", encoding="utf-8") as arquivo:
			escritor = csv.DictWriter(arquivo, fieldnames=list(COLUNAS_EXPORT))
			escritor.writeheader()
			for linha in sorted(linhas, key=self._chave):
				escritor.writerow({**linha, **self._derivadas(linha)})

		return destino

	@staticmethod
	def _chave(linha: dict[str, str]) -> tuple[str, int]:
		return linha["participante"], int(linha["ordem"])

	@staticmethod
	def _derivadas(linha: dict[str, str]) -> dict[str, str]:
		total = int(linha["testes_total"])
		passando = int(linha["testes_passando"])
		taxa = passando / total if total else 0.0
		return {"taxa_sucesso": f"{taxa:.4f}", "testes_falhando": str(total - passando)}
