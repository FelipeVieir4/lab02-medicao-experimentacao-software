from __future__ import annotations

import unittest

from src.domain.entities.measurement import Measurement


class TestMeasurement(unittest.TestCase):
	def test_taxa_de_sucesso_normaliza_pelo_total_de_testes(self):
		medicao = Measurement(tempo_segundos=600, censurado=False, testes_total=8, testes_passando=6)
		self.assertAlmostEqual(medicao.taxa_sucesso, 0.75)
		self.assertEqual(medicao.testes_falhando, 2)

	def test_taxa_de_sucesso_nao_estoura_quando_nenhum_teste_rodou(self):
		medicao = Measurement(tempo_segundos=2100, censurado=True, testes_total=0, testes_passando=0)
		self.assertEqual(medicao.taxa_sucesso, 0.0)
		self.assertFalse(medicao.passou_tudo)

	def test_passou_tudo_so_quando_todos_os_testes_passam(self):
		completo = Measurement(tempo_segundos=300, censurado=False, testes_total=5, testes_passando=5)
		parcial = Measurement(tempo_segundos=300, censurado=True, testes_total=5, testes_passando=4)
		self.assertTrue(completo.passou_tudo)
		self.assertFalse(parcial.passou_tudo)

	def test_recusa_mais_testes_passando_do_que_o_total(self):
		with self.assertRaises(ValueError):
			Measurement(tempo_segundos=100, censurado=False, testes_total=3, testes_passando=4)


if __name__ == "__main__":
	unittest.main()
