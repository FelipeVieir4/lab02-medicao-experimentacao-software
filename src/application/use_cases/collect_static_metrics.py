from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...infrastructure.metrics.duplication_adapter import JscpdDuplicationAdapter
from ...infrastructure.metrics.radon_adapter import RadonAdapter
from ...infrastructure.persistence.metrics_repository import CsvMetricsRepository
from ...infrastructure.persistence.trial_repository import CsvTrialRepository


@dataclass(frozen=True)
class ResultadoColeta:
	destino: Path
	analisados: int
	com_problema: list[str]


class CollectStaticMetrics:
	"""Roda Radon e jscpd sobre o codigo final de cada trial ja registrado.

	Roda em lote, depois dos trials: as metricas saem do arquivo arquivado em data/raw,
	que nao muda mais, entao coletar agora ou daqui a uma semana da o mesmo resultado.
	"""

	def __init__(
		self,
		trials: CsvTrialRepository,
		metricas: CsvMetricsRepository,
		raiz_projeto: Path,
		radon: RadonAdapter | None = None,
		duplicacao: JscpdDuplicationAdapter | None = None,
	) -> None:
		self._trials = trials
		self._metricas = metricas
		self._raiz = Path(raiz_projeto)
		self._radon = radon or RadonAdapter()
		self._duplicacao = duplicacao or JscpdDuplicationAdapter()

	def execute(self) -> ResultadoColeta:
		linhas: list[dict[str, str]] = []
		problemas: list[str] = []

		for trial in self._trials.read_all():
			arquivo = self._raiz / trial["arquivo_solucao"]
			identificacao = f"{trial['participante']}/{trial['kata_id']}"

			if not arquivo.is_file():
				problemas.append(f"{identificacao}: arquivo nao encontrado ({arquivo})")
				continue

			radon = self._radon.analisar(arquivo)
			duplicacao = self._duplicacao.analisar(arquivo)

			observacao = "; ".join(parte for parte in (radon.erro, duplicacao.erro) if parte)
			if observacao:
				problemas.append(f"{identificacao}: {observacao}")

			linhas.append(
				{
					"participante": trial["participante"],
					"ordem": trial["ordem"],
					"kata_id": trial["kata_id"],
					"tratamento": trial["tratamento"],
					"arquivo": trial["arquivo_solucao"],
					"funcoes": str(radon.funcoes),
					"cc_media": self._numero(radon.cc_media),
					"cc_max": "" if radon.cc_max is None else str(radon.cc_max),
					"loc": str(radon.loc),
					"sloc": str(radon.sloc),
					"comentarios": str(radon.comentarios),
					"mi": self._numero(radon.mi),
					"duplicacao_pct": self._numero(duplicacao.percentual),
					"linhas_duplicadas": "" if duplicacao.linhas_duplicadas is None else str(duplicacao.linhas_duplicadas),
					"observacao": observacao,
				}
			)

		destino = self._metricas.salvar(linhas)
		return ResultadoColeta(destino=destino, analisados=len(linhas), com_problema=problemas)

	@staticmethod
	def _numero(valor: float | None) -> str:
		return "" if valor is None else f"{valor:.2f}"
