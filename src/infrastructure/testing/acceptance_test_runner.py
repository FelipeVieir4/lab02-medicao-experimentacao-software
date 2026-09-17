from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

SHIM_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class TestOutcome:
	total: int
	passando: int
	saida: str

	@property
	def rodou(self) -> bool:
		"""Total zero quer dizer que nenhuma assercao chegou a ser executada, normalmente
		porque o arquivo de solucao nem importou (erro de sintaxe, funcao com outro nome)."""
		return self.total > 0


class AcceptanceTestRunner:
	"""Roda os testes de aceitacao do kata sobre o arquivo de solucao do trial.

	A solucao e copiada para uma pasta temporaria como `solution.py`, que e o nome que
	os testes do Codewars importam. Assim o arquivo de teste colado da plataforma
	funciona sem edicao, e o arquivo original do participante nunca e tocado.
	"""

	def __init__(self, timeout_segundos: int = 120) -> None:
		self._timeout = timeout_segundos

	def run(self, arquivo_solucao: Path, arquivo_testes: Path) -> TestOutcome:
		if not arquivo_solucao.is_file():
			raise FileNotFoundError(f"Arquivo de solucao nao encontrado: {arquivo_solucao}")
		if not arquivo_testes.is_file():
			raise FileNotFoundError(f"Arquivo de testes nao encontrado: {arquivo_testes}")

		with tempfile.TemporaryDirectory(prefix="trial-") as pasta:
			area = Path(pasta)
			shutil.copyfile(arquivo_solucao, area / "solution.py")
			shutil.copyfile(arquivo_testes, area / "testes.py")
			relatorio = area / "relatorio.json"

			ambiente = os.environ.copy()
			ambiente["TRIAL_TEST_REPORT"] = str(relatorio)
			ambiente["PYTHONPATH"] = os.pathsep.join([str(area), str(SHIM_DIR)])
			ambiente["PYTHONDONTWRITEBYTECODE"] = "1"

			try:
				processo = subprocess.run(
					[sys.executable, str(area / "testes.py")],
					capture_output=True,
					text=True,
					timeout=self._timeout,
					env=ambiente,
					cwd=str(area),
				)
				saida = processo.stdout + processo.stderr
			except subprocess.TimeoutExpired:
				return TestOutcome(0, 0, f"Os testes passaram de {self._timeout}s e foram interrompidos.")

			if not relatorio.is_file():
				return TestOutcome(0, 0, saida)

			dados = json.loads(relatorio.read_text(encoding="utf-8"))
			return TestOutcome(int(dados["total"]), int(dados["passando"]), saida)
