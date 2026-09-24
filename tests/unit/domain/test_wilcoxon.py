from __future__ import annotations

import unittest

from src.domain.services.wilcoxon import quartis, wilcoxon_pareado

# Valores conferidos contra scipy.stats.wilcoxon(method="exact").
CASOS_CONHECIDOS = [
	([-120, -300, -45, -600, -90, -210], 0.03125),
	([-120, 300, -45, -600, 90, -210], 0.5625),
	([-5, -8, -3, -11, -2, -7, -9, -1], 0.0078125),
	([-120, -300, -45, -600, -90, 210], 0.21875),
	([1.0, -2.0, 3.0, -4.0], 0.875),
]


class TestWilcoxonPareado(unittest.TestCase):
	def test_p_valor_bate_com_o_teste_exato_de_referencia(self):
		for diferencas, esperado in CASOS_CONHECIDOS:
			with self.subTest(diferencas=diferencas):
				resultado = wilcoxon_pareado(diferencas)
				self.assertAlmostEqual(resultado.p_valor, esperado, places=10)

	def test_seis_pares_na_mesma_direcao_atingem_o_menor_p_possivel(self):
		resultado = wilcoxon_pareado([-1, -2, -3, -4, -5, -6])
		self.assertAlmostEqual(resultado.p_valor, 0.03125)
		self.assertAlmostEqual(resultado.menor_p_possivel, 0.03125)
		self.assertTrue(resultado.significativo_a_5)

	def test_diferenca_zero_e_descartada_e_encolhe_o_n(self):
		resultado = wilcoxon_pareado([0, 0, -10, -20, -30, 0])
		self.assertEqual(resultado.n_pares, 6)
		self.assertEqual(resultado.n_usados, 3)
		self.assertEqual(resultado.descartados_por_empate, 3)
		# com 3 pares nem o melhor caso alcanca 5%
		self.assertFalse(resultado.significativo_a_5)

	def test_sem_nenhuma_diferenca_nao_ha_teste(self):
		self.assertIsNone(wilcoxon_pareado([0, 0, 0]))

	def test_recusa_amostra_grande_demais_para_enumerar(self):
		with self.assertRaises(ValueError):
			wilcoxon_pareado(list(range(1, 25)))


class TestQuartis(unittest.TestCase):
	def test_quartis_de_amostra_par(self):
		self.assertEqual(quartis([1, 2, 3, 4, 5, 6, 7, 8]), (2.5, 4.5, 6.5))

	def test_quartis_de_amostra_impar_excluem_a_mediana(self):
		self.assertEqual(quartis([1, 2, 3, 4, 5]), (1.5, 3.0, 4.5))

	def test_lista_vazia_nao_tem_quartis(self):
		self.assertIsNone(quartis([]))


if __name__ == "__main__":
	unittest.main()
