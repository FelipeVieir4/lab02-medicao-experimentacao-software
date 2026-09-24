"""Linha de comando da coleta de dados do experimento.

    python -m src.presentation.cli plano --participante yan
    python -m src.presentation.cli run --participante yan --kata k1
    python -m src.presentation.cli test --kata k1 --participante yan
    python -m src.presentation.cli export
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from ..application.use_cases.analyze_time_and_defects import AnalyzeTimeAndDefects
from ..application.use_cases.collect_static_metrics import CollectStaticMetrics
from ..application.use_cases.export_experiment_data import ExportExperimentData
from ..application.use_cases.record_trial import RecordTrial
from ..application.use_cases.run_trial import RunTrial
from ..domain.entities.treatment import Treatment
from ..domain.services.measurement_policy import TIME_BOX_SEGUNDOS
from ..domain.services import trial_protocol
from ..infrastructure.metrics.duplication_adapter import JscpdDuplicationAdapter
from ..infrastructure.persistence.metrics_repository import CsvMetricsRepository
from ..infrastructure.persistence.trial_repository import CsvTrialRepository
from ..infrastructure.testing.acceptance_test_runner import AcceptanceTestRunner, TestOutcome

RAIZ = Path(__file__).resolve().parents[2]
PASTA_KATAS = RAIZ / "katas"
PASTA_RAW = RAIZ / "data" / "raw"
PASTA_PROCESSED = RAIZ / "data" / "processed"


def caminho_solucao(kata_id: str, participante: str) -> Path:
	return PASTA_KATAS / kata_id / f"solucao_{participante.strip().lower()}.py"


def caminho_testes(kata_id: str) -> Path:
	return PASTA_KATAS / kata_id / "testes.py"


def preparar_solucao(kata_id: str, participante: str) -> Path:
	"""Cada participante trabalha no proprio arquivo, partindo do mesmo ponto de partida."""
	destino = caminho_solucao(kata_id, participante)
	if destino.exists():
		return destino

	base = PASTA_KATAS / kata_id / "base.py"
	if not base.is_file():
		raise SystemExit(
			f"Falta preparar o kata {kata_id}: nao achei {base}.\n"
			f"Rode 'plano' para ver quais katas sao seus para preparar."
		)

	destino.parent.mkdir(parents=True, exist_ok=True)
	shutil.copyfile(base, destino)
	return destino


def formatar_tempo(segundos: float) -> str:
	minutos, resto = divmod(int(segundos), 60)
	return f"{minutos}min{resto:02d}s"


def comando_plano(args: argparse.Namespace) -> int:
	participante = args.participante.strip().lower()
	print(f"Escala do {participante} (time-box de {TIME_BOX_SEGUNDOS // 60} min por trial):\n")
	for kata in trial_protocol.KATAS:
		tratamento = trial_protocol.tratamento_de(participante, kata.id)
		ordem = trial_protocol.ordem_do_kata(kata.id)
		marca = "Copilot LIGADO " if tratamento is Treatment.AI else "Copilot DESLIGADO"
		print(f"  {ordem}. [{kata.id}] {kata.nome:<32} {marca}")

	print("\nKatas que voce prepara (sao os que voce resolve no manual):")
	for kata in trial_protocol.katas_preparados_por(participante):
		pronto = "ok" if caminho_testes(kata.id).is_file() else "FALTA"
		print(f"  [{pronto:>5}] {kata.id} - {kata.nome} - {kata.url}")
	return 0


def comando_test(args: argparse.Namespace) -> int:
	solucao = preparar_solucao(args.kata, args.participante)
	resultado = AcceptanceTestRunner().run(solucao, caminho_testes(args.kata))
	print(resultado.saida.rstrip())

	if not resultado.rodou:
		print("\nNenhuma assercao rodou. Confira o nome da funcao e os erros acima.")
		return 1

	print(f"\n{resultado.passando} de {resultado.total} testes passando.")
	return 0 if resultado.passando == resultado.total else 1


def comando_run(args: argparse.Namespace) -> int:
	participante = args.participante.strip().lower()
	kata = trial_protocol.kata_por_id(args.kata)
	tratamento = trial_protocol.tratamento_de(participante, kata.id)

	repositorio = CsvTrialRepository(PASTA_RAW)
	if repositorio.ja_registrado(participante, kata.id) and not args.refazer:
		print(f"O trial de {kata.id} do {participante} ja foi registrado. Use --refazer se for proposital.")
		return 1

	solucao = preparar_solucao(kata.id, participante)
	testes = caminho_testes(kata.id)
	if not testes.is_file():
		print(f"Falta o arquivo de testes do kata: {testes}")
		return 1

	print(f"\nKata {kata.id} - {kata.nome}")
	print(f"Tratamento: {tratamento.value}")
	if tratamento is Treatment.AI:
		print("Copilot LIGADO. Nenhuma outra consulta: sem Google, sem Stack Overflow, sem outro chat.")
	else:
		print("Copilot DESLIGADO na extensao, nao apenas ignorado. Tambem sem consulta externa.")
	print(f"Arquivo de trabalho: {solucao}")
	print(f"Time-box: {TIME_BOX_SEGUNDOS // 60} min. Ao estourar, o trial encerra do jeito que estiver.")
	input("\nENTER para comecar a contar...")

	def esperar() -> str:
		print("\nCronometro rodando. Rode os testes em outro terminal com o comando 'test'.")
		input("ENTER quando passar em todos os testes, ou quando o tempo acabar...")
		return input("Observacao do trial (ENTER para deixar em branco): ")

	def avisar_estouro() -> None:
		print("\n*** 35 MINUTOS. Encerre o trial agora, mesmo com teste falhando. ***")

	def revisar(resultado: TestOutcome) -> TestOutcome:
		print(resultado.saida.rstrip())
		print("\nNenhuma assercao rodou (a solucao provavelmente nem importou).")
		total = input("Quantos testes o kata tem no total? ")
		if not total.strip().isdigit():
			raise SystemExit("Sem o total de testes o trial nao pode ser registrado.")
		return TestOutcome(total=int(total), passando=0, saida=resultado.saida)

	caso = RunTrial(
		runner=AcceptanceTestRunner(),
		gravador=RecordTrial(repositorio, PASTA_RAW),
	)
	resultado = caso.execute(
		participante=participante,
		kata_id=kata.id,
		arquivo_solucao=solucao,
		arquivo_testes=testes,
		esperar_encerramento=esperar,
		ao_estourar_time_box=avisar_estouro,
		revisar_resultado=revisar,
	)

	medicao = resultado.trial.medicao
	print(f"\nTempo: {formatar_tempo(medicao.tempo_segundos)}" + (" (censurado no time-box)" if medicao.censurado else ""))
	print(f"Testes: {medicao.testes_passando} de {medicao.testes_total} ({medicao.taxa_sucesso:.0%})")
	print(f"Codigo arquivado em: {resultado.trial.arquivo_solucao}")
	print(f"Registro em: {repositorio.caminho_de(participante)}")
	return 0


def comando_export(args: argparse.Namespace) -> int:
	destino = ExportExperimentData(CsvTrialRepository(PASTA_RAW)).execute(
		PASTA_PROCESSED / "trials.csv"
	)
	print(f"Dataset consolidado em: {destino}")
	return 0


def comando_metricas(args: argparse.Namespace) -> int:
	if not JscpdDuplicationAdapter.disponivel():
		print("Aviso: jscpd nao encontrado, a coluna de duplicacao vai sair vazia.")
		print("Para instalar: npm install -g jscpd\n")

	resultado = CollectStaticMetrics(
		trials=CsvTrialRepository(PASTA_RAW),
		metricas=CsvMetricsRepository(PASTA_PROCESSED / "metrics.csv"),
		raiz_projeto=RAIZ,
	).execute()

	print(f"{resultado.analisados} trials analisados.")
	for problema in resultado.com_problema:
		print(f"  - {problema}")
	print(f"Metricas em: {resultado.destino}")
	return 0


def comando_analise(args: argparse.Namespace) -> int:
	resultado = AnalyzeTimeAndDefects(
		trials=CsvTrialRepository(PASTA_RAW),
		pasta_relatorios=RAIZ / "data" / "reports",
	).execute()

	if resultado.katas_incompletos:
		print(f"Katas sem os dois tratamentos, fora da analise: {', '.join(resultado.katas_incompletos)}")

	for analise in (resultado.tempo, resultado.defeitos):
		teste = analise.teste
		if teste is None:
			motivo = "todas as diferencas deram zero" if analise.pares else "sem pares completos"
			print(f"{analise.rq}: teste nao se aplica ({motivo}).")
			continue
		print(
			f"{analise.rq}: mediana com IA {analise.mediana_ai:.2f} x manual "
			f"{analise.mediana_manual:.2f} | W={teste.estatistica:g} p={teste.p_valor:.4f} "
			f"(n={teste.n_usados}, menor p possivel {teste.menor_p_possivel:.4f})"
		)

	print(f"Relatorio em: {resultado.relatorio}")
	return 0


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(prog="cli", description="Coleta de dados do Lab02.")
	sub = parser.add_subparsers(dest="comando", required=True)

	plano = sub.add_parser("plano", help="mostra a escala de trials e o que voce precisa preparar")
	plano.add_argument("--participante", required=True)
	plano.set_defaults(func=comando_plano)

	teste = sub.add_parser("test", help="roda os testes de aceitacao sem registrar nada")
	teste.add_argument("--participante", required=True)
	teste.add_argument("--kata", required=True)
	teste.set_defaults(func=comando_test)

	run = sub.add_parser("run", help="conduz um trial do inicio ao fim e registra a medicao")
	run.add_argument("--participante", required=True)
	run.add_argument("--kata", required=True)
	run.add_argument("--refazer", action="store_true", help="permite repetir um trial ja registrado")
	run.set_defaults(func=comando_run)

	export = sub.add_parser("export", help="junta os CSVs dos participantes num dataset unico")
	export.set_defaults(func=comando_export)

	metricas = sub.add_parser("metricas", help="roda Radon e jscpd sobre o codigo final dos trials")
	metricas.set_defaults(func=comando_metricas)

	analise = sub.add_parser("analise", help="Wilcoxon pareado das RQ1 e RQ2 (tempo e defeitos)")
	analise.set_defaults(func=comando_analise)

	return parser


def main(argv: list[str] | None = None) -> int:
	args = build_parser().parse_args(argv)
	try:
		return int(args.func(args))
	except (ValueError, FileNotFoundError) as erro:
		print(f"Erro: {erro}")
		return 1


if __name__ == "__main__":
	sys.exit(main())
