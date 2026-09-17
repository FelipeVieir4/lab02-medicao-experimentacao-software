from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RadonMetrics:
	"""Metricas estruturais de um arquivo de solucao.

	`loc` entra sempre junto de complexidade: o enunciado pede LOC como metrica de
	controle porque codigo gerado por IA tende a ser mais verboso, e complexidade sem
	normalizar pelo tamanho leva a conclusao errada.
	"""

	funcoes: int
	cc_media: float | None
	cc_max: int | None
	loc: int
	sloc: int
	comentarios: int
	mi: float | None
	erro: str = ""

	@property
	def valido(self) -> bool:
		return not self.erro


class RadonAdapter:
	"""Le complexidade ciclomatica, LOC e indice de manutenibilidade com o Radon.

	Usa a API Python do Radon em vez de chamar o executavel: evita depender do PATH,
	que varia entre as maquinas da dupla, e devolve o dado ja estruturado.
	"""

	def analisar(self, arquivo: Path) -> RadonMetrics:
		arquivo = Path(arquivo)
		if not arquivo.is_file():
			raise FileNotFoundError(f"Arquivo nao encontrado: {arquivo}")

		try:
			from radon.complexity import cc_visit
			from radon.metrics import mi_visit
			from radon.raw import analyze
		except ImportError:
			raise SystemExit("Radon nao instalado. Rode: pip install radon") from None

		codigo = arquivo.read_text(encoding="utf-8")

		try:
			blocos = cc_visit(codigo)
			bruto = analyze(codigo)
			manutenibilidade = mi_visit(codigo, multi=True)
		except SyntaxError as erro:
			# Trial censurado pode terminar com codigo que nem compila. Isso e um dado
			# legitimo do experimento, entao registra o motivo em vez de quebrar a coleta.
			return RadonMetrics(0, None, None, 0, 0, 0, None, f"codigo nao compila: {erro.msg}")

		complexidades = [bloco.complexity for bloco in blocos]

		return RadonMetrics(
			funcoes=len(complexidades),
			cc_media=(sum(complexidades) / len(complexidades)) if complexidades else None,
			cc_max=max(complexidades) if complexidades else None,
			loc=bruto.loc,
			sloc=bruto.sloc,
			comentarios=bruto.comments,
			mi=manutenibilidade,
		)
