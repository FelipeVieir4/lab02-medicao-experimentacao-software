from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...domain.services.wilcoxon import ResultadoWilcoxon, quartis, wilcoxon_pareado
from ...infrastructure.persistence.trial_repository import CsvTrialRepository


@dataclass(frozen=True)
class Par:
	"""Um kata resolvido nos dois tratamentos, que e a unidade pareada da analise."""

	kata_id: str
	valor_ai: float
	valor_manual: float
	censurado_ai: bool
	censurado_manual: bool

	@property
	def diferenca(self) -> float:
		return self.valor_ai - self.valor_manual


@dataclass(frozen=True)
class Analise:
	rq: str
	metrica: str
	unidade: str
	pares: list[Par]
	mediana_ai: float | None
	iqr_ai: tuple[float, float, float] | None
	mediana_manual: float | None
	iqr_manual: tuple[float, float, float] | None
	teste: ResultadoWilcoxon | None


@dataclass(frozen=True)
class ResultadoAnalise:
	tempo: Analise
	defeitos: Analise
	censurados_ai: int
	censurados_manual: int
	katas_incompletos: list[str]
	relatorio: Path


class AnalyzeTimeAndDefects:
	"""Analise das RQ1 (tempo) e RQ2 (defeitos) — Passo 4 do enunciado.

	O pareamento e por kata: o trial com IA de um integrante contra o trial manual do
	outro no mesmo kata. Nao e o pareamento within-subject puro, ja que cada pessoa
	resolve cada kata uma vez so, mas o contrabalanceamento distribui o efeito de
	pessoa igualmente entre os dois tratamentos. Isso precisa constar no relatorio.
	"""

	def __init__(self, trials: CsvTrialRepository, pasta_relatorios: Path) -> None:
		self._trials = trials
		self._pasta = Path(pasta_relatorios)

	def execute(self) -> ResultadoAnalise:
		linhas = self._trials.read_all()
		por_kata: dict[str, dict[str, dict[str, str]]] = {}
		for linha in linhas:
			por_kata.setdefault(linha["kata_id"], {})[linha["tratamento"]] = linha

		completos = {k: v for k, v in por_kata.items() if {"AI", "MANUAL"} <= set(v)}
		incompletos = sorted(set(por_kata) - set(completos))

		tempo = self._analisar(
			completos,
			rq="RQ1",
			metrica="tempo ate passar nos testes (time-to-green)",
			unidade="segundos",
			extrair=lambda linha: float(linha["tempo_segundos"]),
		)
		defeitos = self._analisar(
			completos,
			rq="RQ2",
			metrica="taxa de sucesso ao fim do time-box",
			unidade="proporcao de testes passando",
			extrair=self._taxa_sucesso,
		)

		censurados_ai = sum(1 for v in completos.values() if v["AI"]["censurado"] == "true")
		censurados_manual = sum(1 for v in completos.values() if v["MANUAL"]["censurado"] == "true")

		relatorio = self._escrever_relatorio(tempo, defeitos, censurados_ai, censurados_manual, incompletos)

		return ResultadoAnalise(
			tempo=tempo,
			defeitos=defeitos,
			censurados_ai=censurados_ai,
			censurados_manual=censurados_manual,
			katas_incompletos=incompletos,
			relatorio=relatorio,
		)

	@staticmethod
	def _taxa_sucesso(linha: dict[str, str]) -> float:
		total = int(linha["testes_total"])
		return int(linha["testes_passando"]) / total if total else 0.0

	def _analisar(self, completos, rq, metrica, unidade, extrair) -> Analise:
		pares = [
			Par(
				kata_id=kata_id,
				valor_ai=extrair(trials["AI"]),
				valor_manual=extrair(trials["MANUAL"]),
				censurado_ai=trials["AI"]["censurado"] == "true",
				censurado_manual=trials["MANUAL"]["censurado"] == "true",
			)
			for kata_id, trials in sorted(completos.items())
		]

		valores_ai = [par.valor_ai for par in pares]
		valores_manual = [par.valor_manual for par in pares]

		return Analise(
			rq=rq,
			metrica=metrica,
			unidade=unidade,
			pares=pares,
			mediana_ai=quartis(valores_ai)[1] if valores_ai else None,
			iqr_ai=quartis(valores_ai),
			mediana_manual=quartis(valores_manual)[1] if valores_manual else None,
			iqr_manual=quartis(valores_manual),
			teste=wilcoxon_pareado([par.diferenca for par in pares]) if pares else None,
		)

	def _escrever_relatorio(self, tempo, defeitos, censurados_ai, censurados_manual, incompletos) -> Path:
		self._pasta.mkdir(parents=True, exist_ok=True)
		destino = self._pasta / "analise_rq1_rq2.md"

		partes = ["# Análise das RQ1 e RQ2", ""]
		partes.append(
			"Pareamento por kata: o trial com IA de um integrante contra o trial manual "
			"do outro, no mesmo kata. Teste de Wilcoxon exato para amostras pareadas, "
			"com descritivas em mediana e IQR."
		)
		partes.append("")

		if incompletos:
			partes.append(f"Katas sem os dois tratamentos, fora da análise: {', '.join(incompletos)}.")
			partes.append("")

		partes.append(f"Trials censurados no time-box: {censurados_ai} com IA, {censurados_manual} manuais.")
		partes.append("")

		for analise in (tempo, defeitos):
			partes.extend(self._secao(analise))

		destino.write_text("\n".join(partes), encoding="utf-8")
		return destino

	@staticmethod
	def _secao(analise: Analise) -> list[str]:
		linhas = [f"## {analise.rq} — {analise.metrica}", ""]

		if not analise.pares:
			return linhas + ["Sem pares completos para analisar.", ""]

		def formatar(iqr):
			return f"Q1 {iqr[0]:.2f} | mediana {iqr[1]:.2f} | Q3 {iqr[2]:.2f}" if iqr else "—"

		linhas.append(f"Com IA ({analise.unidade}): {formatar(analise.iqr_ai)}")
		linhas.append(f"Manual ({analise.unidade}): {formatar(analise.iqr_manual)}")
		linhas.append("")
		linhas.append("| Kata | Com IA | Manual | Diferença (IA − manual) |")
		linhas.append("|---|---:|---:|---:|")
		for par in analise.pares:
			linhas.append(
				f"| {par.kata_id} | {par.valor_ai:.2f} | {par.valor_manual:.2f} | {par.diferenca:+.2f} |"
			)
		linhas.append("")

		teste = analise.teste
		if teste is None:
			linhas.append("Todas as diferenças deram zero: o teste de Wilcoxon não se aplica.")
			linhas.append("")
			return linhas

		linhas.append(
			f"Wilcoxon pareado: W = {teste.estatistica:g}, p = {teste.p_valor:.4f} "
			f"({teste.n_usados} de {teste.n_pares} pares; "
			f"{teste.descartados_por_empate} descartado(s) por diferença zero)."
		)
		linhas.append(
			f"Com {teste.n_usados} pares, o menor p-valor que este teste pode produzir é "
			f"{teste.menor_p_possivel:.4f} — o limite vem do tamanho amostral, não dos dados."
		)
		veredito = "rejeita" if teste.significativo_a_5 else "não rejeita"
		linhas.append(f"Ao nível de 5%, {veredito} a hipótese nula.")
		linhas.append("")
		return linhas
