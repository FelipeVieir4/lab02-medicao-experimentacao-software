from __future__ import annotations

from dataclasses import dataclass
from itertools import product

LIMITE_ENUMERACAO = 20


@dataclass(frozen=True)
class ResultadoWilcoxon:
	"""Saida do teste de postos sinalizados de Wilcoxon para amostras pareadas."""

	n_pares: int
	n_usados: int
	w_mais: float
	w_menos: float
	estatistica: float
	p_valor: float
	menor_p_possivel: float
	descartados_por_empate: int

	@property
	def significativo_a_5(self) -> bool:
		return self.p_valor < 0.05


def _postos_medios(valores: list[float]) -> list[float]:
	"""Postos de 1 a n, com posto medio para valores empatados."""
	indexados = sorted(range(len(valores)), key=lambda i: valores[i])
	postos = [0.0] * len(valores)

	inicio = 0
	while inicio < len(indexados):
		fim = inicio
		while fim + 1 < len(indexados) and valores[indexados[fim + 1]] == valores[indexados[inicio]]:
			fim += 1
		posto_medio = (inicio + fim) / 2 + 1
		for posicao in range(inicio, fim + 1):
			postos[indexados[posicao]] = posto_medio
		inicio = fim + 1

	return postos


def wilcoxon_pareado(diferencas: list[float]) -> ResultadoWilcoxon | None:
	"""Teste exato de Wilcoxon para amostras pareadas.

	Exato por enumeracao das 2^n atribuicoes de sinal, e nao pela aproximacao normal:
	com N pequeno (aqui sao 6 pares) a aproximacao nao vale. Diferencas iguais a zero
	sao descartadas, como manda o procedimento classico — o que reduz ainda mais o N e
	por isso vem reportado no resultado.

	Devolve None quando nao sobra nenhum par depois de descartar os empates.
	"""
	n_pares = len(diferencas)
	nao_nulas = [d for d in diferencas if d != 0]
	n = len(nao_nulas)
	descartados = n_pares - n

	if n == 0:
		return None
	if n > LIMITE_ENUMERACAO:
		raise ValueError(f"Enumeracao exata so ate {LIMITE_ENUMERACAO} pares; recebi {n}.")

	postos = _postos_medios([abs(d) for d in nao_nulas])
	w_mais = sum(posto for posto, d in zip(postos, nao_nulas) if d > 0)
	w_menos = sum(posto for posto, d in zip(postos, nao_nulas) if d < 0)
	estatistica = min(w_mais, w_menos)

	# Sob a hipotese nula cada diferenca tem a mesma chance de ser positiva ou negativa,
	# entao a distribuicao de W+ sai de percorrer todas as combinacoes de sinal.
	distribuicao: list[float] = []
	for sinais in product((0, 1), repeat=n):
		distribuicao.append(sum(posto for posto, sinal in zip(postos, sinais) if sinal))

	total = len(distribuicao)
	cauda_baixa = sum(1 for valor in distribuicao if valor <= estatistica) / total
	cauda_alta = sum(1 for valor in distribuicao if valor >= (w_mais + w_menos) - estatistica) / total
	p_valor = min(1.0, cauda_baixa + cauda_alta)

	return ResultadoWilcoxon(
		n_pares=n_pares,
		n_usados=n,
		w_mais=w_mais,
		w_menos=w_menos,
		estatistica=estatistica,
		p_valor=p_valor,
		menor_p_possivel=2 / (2**n),
		descartados_por_empate=descartados,
	)


def mediana(valores: list[float]) -> float | None:
	if not valores:
		return None
	ordenados = sorted(valores)
	meio = len(ordenados) // 2
	if len(ordenados) % 2:
		return ordenados[meio]
	return (ordenados[meio - 1] + ordenados[meio]) / 2


def quartis(valores: list[float]) -> tuple[float, float, float] | None:
	"""Q1, mediana e Q3 pelo metodo da mediana das metades (exclusivo).

	O enunciado pede mediana e IQR no lugar de media e desvio-padrao nas descritivas,
	porque com N pequeno a media e puxada por qualquer outlier.
	"""
	if not valores:
		return None

	ordenados = sorted(valores)
	meio = len(ordenados) // 2
	metade_baixa = ordenados[:meio]
	metade_alta = ordenados[meio + 1:] if len(ordenados) % 2 else ordenados[meio:]

	q1 = mediana(metade_baixa) if metade_baixa else ordenados[0]
	q3 = mediana(metade_alta) if metade_alta else ordenados[-1]

	return (float(q1), float(mediana(ordenados)), float(q3))
