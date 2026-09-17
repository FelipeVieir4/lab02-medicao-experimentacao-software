from __future__ import annotations

import csv
from pathlib import Path

from ...domain.entities.trial import COLUNAS, Trial


class CsvTrialRepository:
	"""Guarda os trials em CSV, um arquivo por participante.

	Arquivo separado por participante de proposito: os dois commitam no mesmo repo e
	um arquivo unico daria conflito de merge a cada trial registrado. A juncao dos
	dois acontece depois, no export.
	"""

	def __init__(self, pasta_raw: Path) -> None:
		self._pasta = Path(pasta_raw)

	def caminho_de(self, participante: str) -> Path:
		return self._pasta / f"trials_{participante.strip().lower()}.csv"

	def append(self, trial: Trial) -> Path:
		destino = self.caminho_de(trial.participante)
		destino.parent.mkdir(parents=True, exist_ok=True)
		novo = not destino.exists()

		with destino.open("a", newline="", encoding="utf-8") as arquivo:
			escritor = csv.DictWriter(arquivo, fieldnames=list(COLUNAS))
			if novo:
				escritor.writeheader()
			escritor.writerow(trial.to_row())

		return destino

	def read_all(self) -> list[dict[str, str]]:
		linhas: list[dict[str, str]] = []
		if not self._pasta.exists():
			return linhas

		for arquivo in sorted(self._pasta.glob("trials_*.csv")):
			with arquivo.open(newline="", encoding="utf-8") as origem:
				linhas.extend(csv.DictReader(origem))

		return linhas

	def ja_registrado(self, participante: str, kata_id: str) -> bool:
		"""Evita registrar o mesmo kata duas vezes para o mesmo participante."""
		alvo = participante.strip().lower()
		return any(
			linha["participante"].strip().lower() == alvo and linha["kata_id"] == kata_id
			for linha in self.read_all()
		)
