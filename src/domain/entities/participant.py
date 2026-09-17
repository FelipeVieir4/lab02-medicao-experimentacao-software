from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Participant:
	"""Um integrante da dupla. No desenho within-subject, cada um passa pelos dois tratamentos."""

	id: str
	nome: str

	def __post_init__(self) -> None:
		if not self.id:
			raise ValueError("Participante precisa de um id.")
