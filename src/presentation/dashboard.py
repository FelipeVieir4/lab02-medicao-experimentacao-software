"""Dashboard Streamlit dos resultados do experimento."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Paleta categorica de dois slots, validada para daltonismo e contraste.
CORES = {"Com IA": "#2a78d6", "Manual": "#eb6834"}
CONECTOR = "#c9c9c4"
TIME_BOX = "#b23a48"
ORDEM_KATAS = ["k1", "k2", "k3", "k4", "k5", "k6"]

RAIZ = Path(__file__).resolve().parents[2]
TRIALS = RAIZ / "data" / "processed" / "trials.csv"
METRICAS = RAIZ / "data" / "processed" / "metrics.csv"

st.set_page_config(page_title="Lab02 | Resultados", page_icon="", layout="wide")
sns.set_theme(style="whitegrid", palette="Set2")


def carregar_dados() -> tuple[pd.DataFrame, pd.DataFrame]:
	if not TRIALS.is_file() or not METRICAS.is_file():
		st.error("Execute 'export' e 'metricas' antes de abrir o dashboard.")
		st.stop()

	trials = pd.read_csv(TRIALS)
	metricas = pd.read_csv(METRICAS)
	trials["tempo_minutos"] = trials["tempo_segundos"] / 60
	trials["taxa_sucesso_pct"] = trials["taxa_sucesso"] * 100
	metricas["tratamento"] = metricas["tratamento"].replace({"AI": "Com IA", "MANUAL": "Manual"})
	trials["tratamento_label"] = trials["tratamento"].replace({"AI": "Com IA", "MANUAL": "Manual"})
	return trials, metricas


def formatar_duracao(segundos: float) -> str:
	"""Abaixo de um minuto em segundos, acima em minutos: e como a plateia le.
	O sufixo vai junto em todo rotulo, entao a unidade nunca fica ambigua."""
	if segundos < 60:
		return f"{segundos:.0f} s"
	minutos, resto = divmod(int(round(segundos)), 60)
	return f"{minutos}min{resto:02d}"


def grafico_tempo_pareado(filtrados: pd.DataFrame, time_box: int = 2100):
	"""Dumbbell por kata, em escala logaritmica.

	Log porque os tempos vao de 6 s a 2100 s: no eixo linear os trials com IA viram
	um risco invisivel ao lado dos manuais. Dumbbell porque a analise e pareada por
	kata — a linha entre os dois pontos e a propria diferenca que entra no Wilcoxon.
	"""
	katas = [k for k in ORDEM_KATAS if k in set(filtrados["kata_id"])]
	nomes = filtrados.drop_duplicates("kata_id").set_index("kata_id")["kata_nome"].to_dict()
	posicao = {k: i for i, k in enumerate(katas)}

	fig, ax = plt.subplots(figsize=(11.5, 0.62 * len(katas) + 2.3))

	for kata in katas:
		bloco = filtrados[filtrados["kata_id"] == kata]
		y = posicao[kata]
		if bloco["tratamento_label"].nunique() == 2:
			xs = [bloco.loc[bloco["tratamento_label"] == t, "tempo_segundos"].iloc[0]
				  for t in ("Com IA", "Manual")]
			ax.plot(xs, [y, y], color=CONECTOR, linewidth=2.5, zorder=1, solid_capstyle="round")
		for _, linha in bloco.iterrows():
			ax.scatter(linha["tempo_segundos"], y, s=140, zorder=3,
					   color=CORES[linha["tratamento_label"]],
					   edgecolor="#fcfcfb", linewidth=2)

	# Rotulo em todos os pontos: o grafico e usado em apresentacao, e quem assiste nao
	# deve precisar decodificar escala log ao vivo. Os rotulos ficam do lado de fora do
	# haltere — IA a esquerda, manual a direita — para nao encostar na linha nem um no outro.
	for _, linha in filtrados.iterrows():
		e_ia = linha["tratamento_label"] == "Com IA"
		ax.annotate(
			formatar_duracao(linha["tempo_segundos"]),
			(linha["tempo_segundos"], posicao[linha["kata_id"]]),
			textcoords="offset points", xytext=(-13 if e_ia else 13, 0),
			ha="right" if e_ia else "left", va="center",
			fontsize=9, color="#55554f",
		)

	# folga nas pontas para os rotulos extremos nao serem cortados (eixo log: multiplica)
	menor, maior = filtrados["tempo_segundos"].min(), max(filtrados["tempo_segundos"].max(), time_box)
	ax.set_xlim(menor / 2.6, maior * 2.6)

	ax.axvline(time_box, color=TIME_BOX, linestyle="--", linewidth=1.2)
	ax.text(time_box, -0.06, "time-box 35 min", transform=ax.get_xaxis_transform(),
			color=TIME_BOX, fontsize=9, ha="center", va="top")

	ax.set_xscale("log")
	ax.set_xlabel("Tempo até passar nos testes (segundos, escala log)")
	ax.set_yticks(range(len(katas)))
	ax.set_yticklabels([f"{k}  {nomes.get(k, '')[:34]}" for k in katas], fontsize=9)
	ax.set_ylim(-0.6, len(katas) - 0.4)
	ax.invert_yaxis()
	ax.grid(axis="y", visible=False)

	marcadores = [plt.Line2D([], [], marker="o", linestyle="", markersize=9,
							 markerfacecolor=c, markeredgecolor="#fcfcfb", label=t)
				  for t, c in CORES.items()]
	ax.legend(handles=marcadores, loc="lower center", bbox_to_anchor=(0.5, 1.02),
			  ncol=2, frameon=False, fontsize=9)
	fig.tight_layout()
	return fig


def grafico_taxa_sucesso(filtrados: pd.DataFrame):
	"""Taxa de sucesso por kata. Substitui o grafico que punha porcentagem e contagem
	de falhas no mesmo eixo — duas grandezas diferentes nao dividem escala."""
	katas = [k for k in ORDEM_KATAS if k in set(filtrados["kata_id"])]
	ordem_hue = [t for t in CORES if t in set(filtrados["tratamento_label"])]

	fig, ax = plt.subplots(figsize=(11.5, 3.5))
	sns.barplot(data=filtrados, x="kata_id", y="taxa_sucesso_pct", hue="tratamento_label",
				order=katas, hue_order=ordem_hue, palette=CORES, errorbar=None,
				ax=ax, width=0.7)

	# barra de altura zero e ambigua: parece ausencia de dado. Rotula explicitamente.
	# A posicao sai do dado — varrer ax.patches pega retangulos que nao sao barras.
	largura, n_hues = 0.7, len(ordem_hue)
	for _, linha in filtrados[filtrados["taxa_sucesso_pct"] == 0].iterrows():
		h = ordem_hue.index(linha["tratamento_label"])
		deslocamento = (h - (n_hues - 1) / 2) * (largura / n_hues)
		ax.annotate("0%", (katas.index(linha["kata_id"]) + deslocamento, 0),
					textcoords="offset points", xytext=(0, 7), ha="center",
					fontsize=9, color="#55554f")

	ax.set_ylim(0, 108)
	ax.set_xlabel("Kata")
	ax.set_ylabel("Testes passando (%)")
	ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=2, frameon=False, fontsize=9)
	ax.grid(axis="x", visible=False)
	fig.tight_layout()
	return fig


def grafico_metrica_por_kata(metricas_filtradas: pd.DataFrame, coluna: str, titulo: str, eixo_y: str, ax):
	"""Barra pareada por kata para uma metrica estrutural."""
	katas = [k for k in ORDEM_KATAS if k in set(metricas_filtradas["kata_id"])]
	ordem_hue = [t for t in CORES if t in set(metricas_filtradas["tratamento"])]
	sns.barplot(data=metricas_filtradas, x="kata_id", y=coluna, hue="tratamento",
				order=katas, hue_order=ordem_hue, palette=CORES,
				errorbar=None, ax=ax, width=0.7)
	ax.set_title(titulo)
	ax.set_xlabel("Kata")
	ax.set_ylabel(eixo_y)
	ax.grid(axis="x", visible=False)
	ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.08), ncol=2, frameon=False, fontsize=9)


def grafico_inversao_por_participante(metricas_filtradas: pd.DataFrame, coluna: str = "loc"):
	"""Slope chart do valor mediano de cada participante nos dois tratamentos.

	O efeito agregado esconde que a direcao muda de pessoa para pessoa. Duas linhas
	que se cruzam mostram isso de imediato — e a cor continua significando tratamento,
	entao a identidade do participante vai no rotulo, nao na cor.
	"""
	resumo = metricas_filtradas.groupby(["participante", "tratamento"])[coluna].median().reset_index()
	eixo_x = {"Com IA": 0, "Manual": 1}

	fig, ax = plt.subplots(figsize=(7.5, 4.6))
	for participante in sorted(resumo["participante"].unique()):
		bloco = resumo[resumo["participante"] == participante]
		pontos = [(eixo_x[t], bloco.loc[bloco["tratamento"] == t, coluna].iloc[0], t)
				  for t in ("Com IA", "Manual") if t in set(bloco["tratamento"])]
		if len(pontos) == 2:
			ax.plot([p[0] for p in pontos], [p[1] for p in pontos],
					color=CONECTOR, linewidth=2.5, zorder=1, solid_capstyle="round")
			ax.annotate(participante, (pontos[-1][0], pontos[-1][1]),
						xytext=(12, 0), textcoords="offset points", va="center",
						fontsize=10, color="#3d3d38")
		for x, y, tratamento in pontos:
			ax.scatter(x, y, s=160, color=CORES[tratamento], edgecolor="#fcfcfb",
					   linewidth=2, zorder=3)
			ax.annotate(f"{y:.0f}", (x, y), xytext=(0, 13), textcoords="offset points",
						ha="center", fontsize=9, color="#55554f")

	ax.set_xticks([0, 1])
	ax.set_xticklabels(["Com IA", "Manual"])
	ax.set_xlim(-0.35, 1.5)
	ax.set_ylabel("LOC mediano")
	ax.set_xlabel("")
	ax.grid(axis="x", visible=False)
	fig.tight_layout()
	return fig


trials, metricas = carregar_dados()

st.title("Lab02 | Assistente de IA versus codificação manual")
st.caption("Painel exploratório dos 12 trials, resultados funcionais e métricas estáticas.")

with st.sidebar:
	st.header("Filtros")
	tratamentos = st.multiselect(
		"Tratamento",
		options=["Com IA", "Manual"],
		default=["Com IA", "Manual"],
	)
	participantes = st.multiselect(
		"Participante",
		options=sorted(trials["participante"].unique()),
		default=sorted(trials["participante"].unique()),
	)

filtrados = trials[
	trials["tratamento_label"].isin(tratamentos) & trials["participante"].isin(participantes)
].copy()
metricas_filtradas = metricas[
	metricas["tratamento"].isin(tratamentos) & metricas["participante"].isin(participantes)
].copy()

if filtrados.empty:
	st.warning("Selecione pelo menos um tratamento e um participante.")
	st.stop()

colunas = st.columns(4)
colunas[0].metric("Trials", len(filtrados))
colunas[1].metric("Mediana do tempo", f"{filtrados['tempo_segundos'].median():.1f} s")
colunas[2].metric("Mediana de sucesso", f"{filtrados['taxa_sucesso_pct'].median():.1f}%")
colunas[3].metric("Censurados", int(filtrados["censurado"].sum()))

st.subheader("Tempo por kata: com IA versus manual")
st.caption(
	"Cada linha liga os dois tratamentos do mesmo kata — é esse par que entra no teste de "
	"Wilcoxon. Escala logarítmica porque os tempos variam de segundos a dezenas de minutos."
)
fig = grafico_tempo_pareado(filtrados)
st.pyplot(fig)
plt.close(fig)

st.subheader("Taxa de sucesso por kata")
fig = grafico_taxa_sucesso(filtrados)
st.pyplot(fig)
plt.close(fig)

st.subheader("Estrutura do código")
# Mesma paleta dos graficos de cima: a cor tem que significar a mesma coisa na pagina
# inteira, senao laranja vira "Manual" num grafico e "Com IA" no outro.
fig, axes = plt.subplots(1, 2, figsize=(14, 5.2))
grafico_metrica_por_kata(metricas_filtradas, "cc_media",
						 "Complexidade ciclomática por kata", "Complexidade média", axes[0])
grafico_metrica_por_kata(metricas_filtradas, "loc", "LOC por kata", "Linhas", axes[1])
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5))
sns.scatterplot(
	data=metricas_filtradas, x="loc", y="cc_media",
	hue="tratamento", hue_order=[t for t in CORES if t in set(metricas_filtradas["tratamento"])],
	palette=CORES, style="participante", s=150,
	edgecolor="#fcfcfb", linewidth=1.5, ax=ax,
)
ax.set_title("Complexidade média versus LOC")
ax.set_xlabel("LOC")
ax.set_ylabel("Complexidade ciclomática média")
ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), frameon=False, fontsize=9)
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.subheader("O efeito do tratamento muda de direção entre os participantes")
st.caption(
	"Mediana de LOC de cada integrante nas duas condições. As linhas se cruzam: o código "
	"do Felipe com IA é mais curto que o manual dele, e o do Yan é mais longo que o manual "
	"dele. A diferença agregada da RQ3 é a média de duas tendências opostas."
)
fig = grafico_inversao_por_participante(metricas_filtradas)
st.pyplot(fig)
plt.close(fig)

resumo = metricas_filtradas.groupby("tratamento", as_index=False)[
	["cc_media", "cc_max", "loc", "sloc", "mi", "duplicacao_pct"]
].median()
st.subheader("Resumo das métricas estáticas")
st.dataframe(resumo, width="stretch", hide_index=True)

with st.expander("Dados usados no painel"):
	st.dataframe(filtrados, width="stretch", hide_index=True)

st.info(
	"Nota metodológica: os tempos com IA do Felipe foram registrados como tempo de implementação "
	"assistida nesta execução, e não como trials completos conduzidos pelo comando run. "
	"Essa limitação deve ser considerada ao interpretar a RQ1."
)
