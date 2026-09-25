"""Dashboard Streamlit dos resultados do experimento."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

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

st.subheader("Tempo e qualidade funcional")
fig, axes = plt.subplots(1, 2, figsize=(14, 4.8))
sns.barplot(
	data=filtrados,
	x="kata_id",
	y="tempo_minutos",
	hue="tratamento_label",
	errorbar=None,
	ax=axes[0],
)
axes[0].set_title("Tempo por kata")
axes[0].set_xlabel("Kata")
axes[0].set_ylabel("Minutos")
axes[0].axhline(35, color="#b23a48", linestyle="--", linewidth=1, label="Time-box")
axes[0].legend(title="Tratamento")

sucesso = filtrados.groupby("tratamento_label", as_index=False)[["taxa_sucesso_pct", "testes_falhando"]].median()
sucesso_longo = sucesso.melt("tratamento_label", var_name="metrica", value_name="valor")
sns.barplot(data=sucesso_longo, x="tratamento_label", y="valor", hue="metrica", errorbar=None, ax=axes[1])
axes[1].set_title("Medianas de sucesso e falhas")
axes[1].set_xlabel("")
axes[1].set_ylabel("Valor")
axes[1].legend(title="Métrica", labels=["Taxa de sucesso (%)", "Testes falhando"])
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.subheader("Estrutura do código")
fig, axes = plt.subplots(1, 2, figsize=(14, 4.8))
sns.barplot(data=metricas_filtradas, x="kata_id", y="loc", hue="tratamento", errorbar=None, ax=axes[0])
axes[0].set_title("LOC por kata")
axes[0].set_xlabel("Kata")
axes[0].set_ylabel("Linhas")

sns.scatterplot(
	data=metricas_filtradas,
	x="loc",
	y="cc_media",
	hue="tratamento",
	style="participante",
	s=130,
	ax=axes[1],
)
axes[1].set_title("Complexidade média versus LOC")
axes[1].set_xlabel("LOC")
axes[1].set_ylabel("Complexidade ciclomática média")
axes[1].legend(title="Tratamento / participante")
plt.tight_layout()
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
