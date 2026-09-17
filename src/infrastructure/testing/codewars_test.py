"""Shim do modulo `codewars_test`.

Os testes de exemplo dos katas do Codewars importam `codewars_test`, que so existe
dentro da plataforma. Este modulo reimplementa a parte usada nos testes de aceitacao
para que eles rodem localmente sem nenhuma edicao: o arquivo de teste e colado do
Codewars exatamente como esta.

Cada assercao conta como um teste de aceitacao. Uma assercao que falha nao interrompe
as seguintes, senao a primeira falha esconderia o resto e a contagem de testes
passando ficaria menor do que a real.
"""

from __future__ import annotations

import atexit
import json
import os
from typing import Any, Callable

_total = 0
_passando = 0
_falhas: list[str] = []


def _registrar(ok: bool, mensagem: str) -> None:
	global _total, _passando
	_total += 1
	if ok:
		_passando += 1
	else:
		_falhas.append(mensagem)
		print(f"  FALHOU: {mensagem}")


def assert_equals(actual: Any, expected: Any, message: str | None = None) -> None:
	_registrar(actual == expected, message or f"esperava {expected!r}, veio {actual!r}")


def assert_not_equals(actual: Any, unexpected: Any, message: str | None = None) -> None:
	_registrar(actual != unexpected, message or f"nao esperava {unexpected!r}")


def assert_approx_equals(
	actual: float,
	expected: float,
	margin: float = 1e-9,
	message: str | None = None,
) -> None:
	ok = abs(actual - expected) <= margin
	_registrar(ok, message or f"esperava ~{expected!r}, veio {actual!r}")


def expect(passed: bool, message: str | None = None) -> None:
	_registrar(bool(passed), message or "expect recebeu valor falso")


def fail(message: str = "falhou") -> None:
	_registrar(False, message)


def pass_(message: str = "passou") -> None:
	_registrar(True, message)


def describe(text: str) -> Callable[[Callable[[], None]], Callable[[], None]]:
	def decorator(fn: Callable[[], None]) -> Callable[[], None]:
		print(text)
		fn()
		return fn

	return decorator


def it(text: str) -> Callable[[Callable[[], None]], Callable[[], None]]:
	def decorator(fn: Callable[[], None]) -> Callable[[], None]:
		print(f"- {text}")
		try:
			fn()
		except Exception as erro:  # a solucao estourou: conta como uma assercao falha
			_registrar(False, f"{text}: {type(erro).__name__}: {erro}")
		return fn

	return decorator


def resumo() -> dict[str, int]:
	return {"total": _total, "passando": _passando, "falhas": len(_falhas)}


@atexit.register
def _gravar_relatorio() -> None:
	destino = os.environ.get("TRIAL_TEST_REPORT")
	if not destino:
		return
	with open(destino, "w", encoding="utf-8") as arquivo:
		json.dump({**resumo(), "detalhe_falhas": _falhas}, arquivo, ensure_ascii=False)
