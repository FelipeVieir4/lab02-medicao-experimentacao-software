from __future__ import annotations

import unittest

from src.domain.services.measurement_policy import TIME_BOX_SEGUNDOS, aplicar_time_box


class TestAplicarTimeBox(unittest.TestCase):
	def test_trial_que_passa_dentro_do_tempo_nao_e_censurado(self):
		medicao = aplicar_time_box(tempo_decorrido=840, testes_total=6, testes_passando=6)
		self.assertEqual(medicao.tempo_segundos, 840)
		self.assertFalse(medicao.censurado)

	def test_trial_que_estoura_o_time_box_entra_censurado_e_nao_descartado(self):
		medicao = aplicar_time_box(tempo_decorrido=2400, testes_total=6, testes_passando=4)
		self.assertEqual(medicao.tempo_segundos, TIME_BOX_SEGUNDOS)
		self.assertTrue(medicao.censurado)
		self.assertEqual(medicao.testes_passando, 4)

	def test_parar_antes_do_tempo_sem_passar_em_tudo_tambem_e_censura(self):
		medicao = aplicar_time_box(tempo_decorrido=900, testes_total=6, testes_passando=5)
		self.assertTrue(medicao.censurado)
		self.assertEqual(medicao.tempo_segundos, 900)

	def test_tempo_nunca_passa_do_time_box_no_registro(self):
		medicao = aplicar_time_box(tempo_decorrido=9999, testes_total=6, testes_passando=6)
		self.assertEqual(medicao.tempo_segundos, TIME_BOX_SEGUNDOS)
		self.assertTrue(medicao.censurado)


if __name__ == "__main__":
	unittest.main()
