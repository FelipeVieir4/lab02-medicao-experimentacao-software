from __future__ import annotations

from ..entities.measurement import Measurement

TIME_BOX_SEGUNDOS = 35 * 60


def aplicar_time_box(
	tempo_decorrido: float,
	testes_total: int,
	testes_passando: int,
	time_box: int = TIME_BOX_SEGUNDOS,
) -> Measurement:
	"""Fecha a medicao do trial respeitando o time-box.

	Trial que nao chega a passar em todos os testes dentro do tempo entra como
	censurado no valor do time-box, e nao descartado: descartar distorceria a
	comparacao a favor do tratamento que falha mais.
	"""
	if tempo_decorrido < 0:
		raise ValueError("Tempo decorrido nao pode ser negativo.")

	passou_tudo = testes_total > 0 and testes_passando == testes_total
	estourou = tempo_decorrido >= time_box
	censurado = estourou or not passou_tudo

	return Measurement(
		tempo_segundos=min(tempo_decorrido, float(time_box)),
		censurado=censurado,
		testes_total=testes_total,
		testes_passando=testes_passando,
	)
