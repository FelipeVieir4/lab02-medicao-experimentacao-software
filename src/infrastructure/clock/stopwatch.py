from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from time import monotonic
from typing import Callable


@dataclass(frozen=True)
class StopwatchResult:
	started_at: datetime
	stopped_at: datetime
	elapsed_seconds: float


class Stopwatch:
	def __init__(self, clock: Callable[[], float] = monotonic) -> None:
		self._clock = clock
		self._started_at: datetime | None = None
		self._stopped_at: datetime | None = None
		self._started_tick: float | None = None
		self._elapsed_seconds: float | None = None

	@property
	def is_running(self) -> bool:
		return self._started_tick is not None and self._elapsed_seconds is None

	@property
	def elapsed_seconds(self) -> float:
		if self._started_tick is None:
			return 0.0
		if self._elapsed_seconds is not None:
			return self._elapsed_seconds
		return self._clock() - self._started_tick

	def start(self) -> None:
		if self.is_running:
			raise RuntimeError("O cronometro ja foi iniciado.")

		self._started_at = datetime.now(timezone.utc)
		self._started_tick = self._clock()
		self._stopped_at = None
		self._elapsed_seconds = None

	def stop(self) -> StopwatchResult:
		if self._started_tick is None or self._started_at is None:
			raise RuntimeError("O cronometro ainda nao foi iniciado.")
		if self._elapsed_seconds is not None or self._stopped_at is not None:
			raise RuntimeError("O cronometro ja foi parado.")

		self._elapsed_seconds = self._clock() - self._started_tick
		self._stopped_at = datetime.now(timezone.utc)

		return StopwatchResult(
			started_at=self._started_at,
			stopped_at=self._stopped_at,
			elapsed_seconds=self._elapsed_seconds,
		)

	def reset(self) -> None:
		self._started_at = None
		self._stopped_at = None
		self._started_tick = None
		self._elapsed_seconds = None
