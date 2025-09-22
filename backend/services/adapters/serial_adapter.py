import os
import asyncio
from typing import AsyncGenerator, Dict, Any, Optional

try:
	import serial
except Exception:
	serial = None


class SerialAdapter:
	def __init__(self) -> None:
		self.port = os.getenv("SERIAL_PORT", "COM3")
		self.baud = int(os.getenv("SERIAL_BAUD", "9600"))
		self._latest: Dict[str, Any] = {}
		self._stop = False
		self._ser = None

	def _open(self) -> None:
		if serial is None:
			return
		try:
			self._ser = serial.Serial(self.port, self.baud, timeout=1)
		except Exception:
			self._ser = None

	def _reader_loop(self) -> None:
		if self._ser is None:
			return
		while not self._stop:
			try:
				line = self._ser.readline().decode(errors="ignore").strip()
				if not line:
					continue
				self._parse_line(line)
			except Exception:
				continue

	def _parse_line(self, data: str) -> None:
		# Expected format: DATA,STATE:FORWARD,DIST:123,ALERT:0
		if not data.startswith("DATA,"):
			return
		pairs = data[5:].split(",")
		result: Dict[str, Any] = {}
		for token in pairs:
			if ":" in token:
				key, value = token.split(":", 1)
				key = key.strip().upper()
				if key == "STATE":
					result["motor_status"] = value
				elif key == "DIST":
					try:
						result["distance_cm"] = int(value)
					except Exception:
						pass
				elif key == "ALERT":
					result["alert_active"] = (value == "1")
		if result:
			self._latest.update(result)

	async def stream(self) -> AsyncGenerator[Dict[str, Any], None]:
		loop = asyncio.get_event_loop()
		self._open()
		if self._ser is not None:
			self._stop = False
			loop.run_in_executor(None, self._reader_loop)
		while True:
			await asyncio.sleep(0.5)
			yield dict(self._latest)

	async def send_command(self, action: str, value: Optional[Any]) -> bool:
		cmd = None
		a = action.lower()
		if a == "forward":
			cmd = "CMD,FORWARD\n"
		elif a == "back":
			cmd = "CMD,BACK\n"
		elif a == "left":
			cmd = "CMD,LEFT\n"
		elif a == "right":
			cmd = "CMD,RIGHT\n"
		elif a == "stop":
			cmd = "CMD,STOP\n"
		elif a == "set_servo" and isinstance(value, (int, float)):
			cmd = f"CMD,SERVO:{int(value)}\n"
		if self._ser is not None and cmd is not None:
			try:
				self._ser.write(cmd.encode())
				return True
			except Exception:
				return False
		return False
