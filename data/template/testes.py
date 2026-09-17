"""Molde do arquivo de testes de aceitacao de um kata.

Copie para katas/<kata_id>/testes.py e cole os Sample Tests do Codewars exatamente
como estao na plataforma, sem adaptar nada. O modulo `codewars_test` existe aqui
(src/infrastructure/testing/codewars_test.py) justamente para que o teste colado rode
sem edicao, e a solucao do participante e importada como `solution`.

Se o kata usar o formato antigo, com unittest.TestCase, troque este molde pelo codigo
de la do mesmo jeito: o runner conta as assercoes independente do formato.
"""

import codewars_test as test

from solution import nome_da_funcao_do_kata


@test.describe("Sample Tests")
def sample_tests():
	@test.it("exemplo do enunciado")
	def exemplo():
		test.assert_equals(nome_da_funcao_do_kata("entrada"), "saida esperada")
