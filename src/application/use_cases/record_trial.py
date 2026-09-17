from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from ...domain.entities.trial import Trial
from ...domain.entities.treatment import Treatment
from ...domain.services.measurement_policy import aplicar_time_box
from ...domain.services.trial_protocol import kata_por_id, ordem_do_kata, tratamento_de
from ...infrastructure.persistence.trial_repository import CsvTrialRepository


class RecordTrial:
	"""Fecha um trial: arquiva o codigo final e grava a linha no CSV.

	O arquivo de solucao e copiado para data/raw no estado em que ficou quando o tempo
	acabou, mesmo com teste falhando. E sobre essa copia que o Radon e o jscpd rodam
	depois, entao ela nao pode ser mexida.
	"""

	def __init__(
		self,
		repositorio: CsvTrialRepository,
		pasta_raw: Path,
		raiz_projeto: Path | None = None,
	) -> None:
		self._repositorio = repositorio
		self._pasta_raw = Path(pasta_raw)
		# O caminho vai para o CSV relativo a raiz do projeto: caminho absoluto gravaria
		# a pasta pessoal de cada maquina e quebraria na hora de rodar as metricas.
		self._raiz = Path(raiz_projeto) if raiz_projeto else self._pasta_raw.parents[1]

	def execute(
		self,
		participante: str,
		kata_id: str,
		inicio: datetime,
		tempo_decorrido: float,
		testes_total: int,
		testes_passando: int,
		arquivo_solucao: Path,
		observacoes: str = "",
	) -> Trial:
		kata = kata_por_id(kata_id)
		tratamento = tratamento_de(participante, kata_id)
		ordem = ordem_do_kata(kata_id)
		medicao = aplicar_time_box(tempo_decorrido, testes_total, testes_passando)

		destino = self._arquivar(participante, ordem, kata_id, tratamento, arquivo_solucao)

		trial = Trial(
			participante=participante.strip().lower(),
			ordem=ordem,
			kata=kata,
			tratamento=tratamento,
			inicio=inicio,
			medicao=medicao,
			arquivo_solucao=self._relativo(destino),
			observacoes=observacoes,
		)

		self._repositorio.append(trial)
		return trial

	def _relativo(self, caminho: Path) -> str:
		try:
			return caminho.relative_to(self._raiz).as_posix()
		except ValueError:
			return caminho.as_posix()

	def _arquivar(
		self,
		participante: str,
		ordem: int,
		kata_id: str,
		tratamento: Treatment,
		arquivo_solucao: Path,
	) -> Path:
		pasta = self._pasta_raw / participante.strip().lower()
		pasta.mkdir(parents=True, exist_ok=True)
		destino = pasta / f"{ordem:02d}_{kata_id}_{tratamento.value.lower()}.py"
		shutil.copyfile(arquivo_solucao, destino)
		return destino
