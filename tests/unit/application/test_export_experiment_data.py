from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from src.application.use_cases.export_experiment_data import ExportExperimentData
from src.domain.entities.trial import COLUNAS
from src.infrastructure.persistence.trial_repository import CsvTrialRepository


class TestExportExperimentData(unittest.TestCase):
	def test_exporta_trials_ordenados_e_calcula_metricas_derivadas(self):
		with tempfile.TemporaryDirectory() as pasta_temporaria:
			pasta_raw = Path(pasta_temporaria) / "raw"
			repositorio = CsvTrialRepository(pasta_raw)
			self._escrever_trials(
				repositorio.caminho_de("yan"),
				[
					self._linha("yan", 1, 4, 4),
					self._linha("yan", 2, 5, 3),
				],
			)
			self._escrever_trials(
				repositorio.caminho_de("felipe"),
				[self._linha("felipe", 1, 0, 0)],
			)

			destino = Path(pasta_temporaria) / "processed" / "trials.csv"
			ExportExperimentData(repositorio).execute(destino)

			with destino.open(newline="", encoding="utf-8") as arquivo:
				linhas = list(csv.DictReader(arquivo))

			self.assertEqual([linha["participante"] for linha in linhas], ["felipe", "yan", "yan"])
			self.assertEqual(linhas[0]["taxa_sucesso"], "0.0000")
			self.assertEqual(linhas[0]["testes_falhando"], "0")
			self.assertEqual(linhas[2]["taxa_sucesso"], "0.6000")
			self.assertEqual(linhas[2]["testes_falhando"], "2")

	@staticmethod
	def _linha(participante: str, ordem: int, testes_total: int, testes_passando: int) -> dict[str, str]:
		return {
			"participante": participante,
			"ordem": str(ordem),
			"kata_id": f"k{ordem}",
			"kata_nome": "Kata de teste",
			"tratamento": "AI",
			"inicio": "2026-09-17T20:00:00+00:00",
			"tempo_segundos": "600.0",
			"censurado": "false",
			"testes_total": str(testes_total),
			"testes_passando": str(testes_passando),
			"arquivo_solucao": "data/raw/solucao.py",
			"observacoes": "",
		}

	@staticmethod
	def _escrever_trials(destino: Path, linhas: list[dict[str, str]]) -> None:
		destino.parent.mkdir(parents=True, exist_ok=True)
		with destino.open("w", newline="", encoding="utf-8") as arquivo:
			escritor = csv.DictWriter(arquivo, fieldnames=list(COLUNAS))
			escritor.writeheader()
			escritor.writerows(linhas)


if __name__ == "__main__":
	unittest.main()
