from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Measurement:
	"""O que sai de um trial: quanto tempo levou e quantos testes passaram no fim."""

	tempo_segundos: float
	censurado: bool
	testes_total: int
	testes_passando: int

	def __post_init__(self) -> None:
		if self.tempo_segundos < 0:
			raise ValueError("Tempo nao pode ser negativo.")
		if self.testes_total < 0 or self.testes_passando < 0:
			raise ValueError("Contagem de testes nao pode ser negativa.")
		if self.testes_passando > self.testes_total:
			raise ValueError(
				f"Passaram {self.testes_passando} testes de um total de {self.testes_total}."
			)

	@property
	def taxa_sucesso(self) -> float:
		"""Metrica primaria da RQ2. Normaliza katas com numeros diferentes de testes."""
		if self.testes_total == 0:
			return 0.0
		return self.testes_passando / self.testes_total

	@property
	def testes_falhando(self) -> int:
		return self.testes_total - self.testes_passando

	@property
	def passou_tudo(self) -> bool:
		return self.testes_total > 0 and self.testes_passando == self.testes_total
