from __future__ import annotations

from ..entities.kata import Kata
from ..entities.treatment import Treatment

AI = Treatment.AI
MANUAL = Treatment.MANUAL

# Os 6 objetos experimentais, na ordem em que os dois integrantes devem resolve-los.
KATAS: tuple[Kata, ...] = (
	Kata("k1", "Connect Four - placing tokens", "https://www.codewars.com/kata/connect-four-placing-tokens"),
	Kata("k2", "Exclamation marks series #17", "https://www.codewars.com/kata/57fb44a12b53146fe1000136"),
	Kata("k3", "If you can read this...", "https://www.codewars.com/kata/586538146b56991861000293"),
	Kata("k4", "Kebabize", "https://www.codewars.com/kata/57f8ff867a28db569e000c4a"),
	Kata("k5", "Buying a car", "https://www.codewars.com/kata/554a44516729e4d80b000012"),
	Kata("k6", "The Vowel Code", "https://www.codewars.com/kata/53697be005f803751e0015aa"),
)

# Contrabalanceamento: cada kata e resolvido uma vez em cada tratamento, e em cada
# posicao da sequencia os dois integrantes estao em tratamentos opostos. Assim o
# efeito de aprendizado/cansaco ao longo dos 6 trials cai igual nos dois tratamentos.
ESCALA: dict[str, dict[str, Treatment]] = {
	"yan": {"k1": AI, "k2": MANUAL, "k3": AI, "k4": MANUAL, "k5": AI, "k6": MANUAL},
	"felipe": {"k1": MANUAL, "k2": AI, "k3": MANUAL, "k4": AI, "k5": MANUAL, "k6": AI},
}


def kata_por_id(kata_id: str) -> Kata:
	for kata in KATAS:
		if kata.id == kata_id:
			return kata
	validos = ", ".join(k.id for k in KATAS)
	raise ValueError(f"Kata desconhecido: {kata_id!r}. Use um de: {validos}.")


def ordem_do_kata(kata_id: str) -> int:
	for posicao, kata in enumerate(KATAS, start=1):
		if kata.id == kata_id:
			return posicao
	raise ValueError(f"Kata desconhecido: {kata_id!r}.")


def tratamento_de(participante: str, kata_id: str) -> Treatment:
	"""Le o tratamento direto da escala, em vez de deixar a pessoa escolher na hora.
	E o que impede alguem rodar o kata errado no tratamento errado por descuido."""
	chave = participante.strip().lower()
	if chave not in ESCALA:
		validos = ", ".join(ESCALA)
		raise ValueError(f"Participante desconhecido: {participante!r}. Use um de: {validos}.")
	escala = ESCALA[chave]
	if kata_id not in escala:
		raise ValueError(f"Kata desconhecido: {kata_id!r}.")
	return escala[kata_id]


def katas_preparados_por(participante: str) -> list[Kata]:
	"""Quem prepara o arquivo de um kata acaba lendo o enunciado antes da hora, o que
	daria vantagem indevida. Por isso cada um prepara justamente os katas que vai
	resolver no MANUAL: a exposicao previa cai sempre contra a hipotese da IA."""
	chave = participante.strip().lower()
	if chave not in ESCALA:
		raise ValueError(f"Participante desconhecido: {participante!r}.")
	return [kata for kata in KATAS if ESCALA[chave][kata.id] is MANUAL]
