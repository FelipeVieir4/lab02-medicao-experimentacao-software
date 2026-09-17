from __future__ import annotations

from enum import Enum


class Treatment(Enum):
	"""Os dois tratamentos do experimento: Copilot ligado ou desligado."""

	AI = "AI"
	MANUAL = "MANUAL"

	@classmethod
	def from_text(cls, valor: str) -> "Treatment":
		try:
			return cls(valor.strip().upper())
		except ValueError:
			validos = ", ".join(t.value for t in cls)
			raise ValueError(f"Tratamento invalido: {valor!r}. Use um de: {validos}.") from None

	def __str__(self) -> str:
		return self.value
