from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Kata:
	"""Um dos objetos experimentais: o kata do Codewars que sera resolvido."""

	id: str
	nome: str
	url: str

	def __post_init__(self) -> None:
		if not self.id:
			raise ValueError("Kata precisa de um id.")
		if not self.nome:
			raise ValueError(f"Kata {self.id} precisa de um nome.")
