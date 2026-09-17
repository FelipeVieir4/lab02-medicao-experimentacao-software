from __future__ import annotations

import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from ...domain.entities.trial import Trial
from ...domain.services.measurement_policy import TIME_BOX_SEGUNDOS
from ...domain.services.trial_protocol import kata_por_id, tratamento_de
from ...infrastructure.clock.stopwatch import Stopwatch
from ...infrastructure.testing.acceptance_test_runner import AcceptanceTestRunner, TestOutcome
from .record_trial import RecordTrial


@dataclass(frozen=True)
class TrialResult:
	trial: Trial
	resultado_testes: TestOutcome


class RunTrial:
	"""Conduz um trial do inicio ao fim: dispara o cronometro, espera a pessoa encerrar,
	roda os testes de aceitacao sobre o codigo final e registra a medicao.

	O tratamento nao e parametro: vem da escala de contrabalanceamento a partir de quem
	esta resolvendo e de qual kata. Isso evita rodar o kata no tratamento errado.
	"""

	def __init__(
		self,
		runner: AcceptanceTestRunner,
		gravador: RecordTrial,
		time_box: int = TIME_BOX_SEGUNDOS,
	) -> None:
		self._runner = runner
		self._gravador = gravador
		self._time_box = time_box

	def execute(
		self,
		participante: str,
		kata_id: str,
		arquivo_solucao: Path,
		arquivo_testes: Path,
		esperar_encerramento: Callable[[], str],
		ao_estourar_time_box: Callable[[], None] | None = None,
		revisar_resultado: Callable[[TestOutcome], TestOutcome] | None = None,
	) -> TrialResult:
		kata = kata_por_id(kata_id)
		tratamento = tratamento_de(participante, kata_id)

		cronometro = Stopwatch()
		inicio = datetime.now(timezone.utc)
		alarme = self._armar_alarme(ao_estourar_time_box)

		cronometro.start()
		try:
			observacoes = esperar_encerramento()
		finally:
			medida = cronometro.stop()
			if alarme is not None:
				alarme.cancel()

		resultado = self._runner.run(arquivo_solucao, arquivo_testes)
		if revisar_resultado is not None and not resultado.rodou:
			# Nenhuma assercao rodou (a solucao nem importou). Quem conduz o trial
			# informa a contagem correta, senao o trial entraria com 0 de 0 testes.
			resultado = revisar_resultado(resultado)

		trial = self._gravador.execute(
			participante=participante,
			kata_id=kata.id,
			inicio=inicio,
			tempo_decorrido=medida.elapsed_seconds,
			testes_total=resultado.total,
			testes_passando=resultado.passando,
			arquivo_solucao=arquivo_solucao,
			observacoes=observacoes,
		)

		assert trial.tratamento is tratamento
		return TrialResult(trial=trial, resultado_testes=resultado)

	def _armar_alarme(self, callback: Callable[[], None] | None) -> threading.Timer | None:
		if callback is None:
			return None
		alarme = threading.Timer(self._time_box, callback)
		alarme.daemon = True
		alarme.start()
		return alarme
