import os
import asyncio
from typing import Dict, Any, Optional
from .adapters.simulation_adapter import SimulationAdapter
from .adapters.serial_adapter import SerialAdapter


class TelemetryManager:
	def __init__(self) -> None:
		adapter_name = os.getenv("ADAPTER", "sim").lower()
		if adapter_name == "serial":
			self.adapter = SerialAdapter()
		else:
			self.adapter = SimulationAdapter()
		self._latest: Dict[str, Any] = {}
		self._lock = asyncio.Lock()

	async def run(self) -> None:
		async for data in self.adapter.stream():
			if not data:
				continue
			async with self._lock:
				self._latest = {**self._latest, **data}

	def get_latest(self) -> Dict[str, Any]:
		return dict(self._latest)

	async def send_command(self, action: str, value: Optional[Any] = None) -> bool:
		return await self.adapter.send_command(action, value)

	async def update_external(self, data: Dict[str, Any]) -> None:
		async with self._lock:
			self._latest = {**self._latest, **data}
