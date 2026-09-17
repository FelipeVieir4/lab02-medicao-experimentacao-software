from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

# Fixo de proposito: o jscpd so considera clone um trecho com pelo menos esse tanto de
# tokens, e mudar o valor muda o resultado. Como as solucoes de kata sao curtas, 20 e
# baixo o suficiente para pegar repeticao real, e tem que ser o MESMO nos 12 trials.
MIN_TOKENS = 20


@dataclass(frozen=True)
class DuplicationMetrics:
	percentual: float | None
	linhas_duplicadas: int | None
	clones: int | None
	erro: str = ""

	@property
	def valido(self) -> bool:
		return not self.erro


class JscpdDuplicationAdapter:
	"""Mede duplicacao de codigo com o jscpd, que faz o papel do CPD do PMD em Python.

	O Radon nao mede duplicacao, e a RQ3 pede complexidade *e* duplicacao — por isso a
	ferramenta extra. Se o jscpd nao estiver instalado, a coleta continua e a duplicacao
	fica vazia com o motivo registrado, em vez de derrubar a coleta inteira.
	"""

	def __init__(self, min_tokens: int = MIN_TOKENS, timeout_segundos: int = 120) -> None:
		self._min_tokens = min_tokens
		self._timeout = timeout_segundos

	@staticmethod
	def disponivel() -> bool:
		return shutil.which("jscpd") is not None

	def analisar(self, arquivo: Path) -> DuplicationMetrics:
		arquivo = Path(arquivo)
		if not arquivo.is_file():
			raise FileNotFoundError(f"Arquivo nao encontrado: {arquivo}")

		executavel = shutil.which("jscpd")
		if executavel is None:
			return DuplicationMetrics(None, None, None, "jscpd nao instalado (npm i -g jscpd)")

		with tempfile.TemporaryDirectory(prefix="jscpd-") as pasta:
			saida = Path(pasta)
			comando = [
				executavel,
				str(arquivo),
				"--reporters", "json",
				"--output", str(saida),
				"--min-tokens", str(self._min_tokens),
				"--format", "python",
				"--silent",
			]

			try:
				subprocess.run(comando, capture_output=True, text=True, timeout=self._timeout)
			except subprocess.TimeoutExpired:
				return DuplicationMetrics(None, None, None, f"jscpd passou de {self._timeout}s")

			relatorio = saida / "jscpd-report.json"
			if not relatorio.is_file():
				return DuplicationMetrics(None, None, None, "jscpd nao gerou relatorio")

			total = json.loads(relatorio.read_text(encoding="utf-8")).get("statistics", {}).get("total", {})

		return DuplicationMetrics(
			percentual=float(total.get("percentage", 0.0)),
			linhas_duplicadas=int(total.get("duplicatedLines", 0)),
			clones=int(total.get("clones", 0)),
		)
