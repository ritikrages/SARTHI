import asyncio
import random
from typing import AsyncGenerator, Dict, Any, Optional


class SimulationAdapter:
	def __init__(self) -> None:
		self.speed = 0.0
		self.distance_cm = 100.0
		self.motor_status = "stopped"
		self.led_states = {"left": False, "right": False, "head": True}
		self.servo_angle = 90
		self.battery_pct = 87
		self.drowsy = False
		self.emotion = "neutral"

	async def stream(self) -> AsyncGenerator[Dict[str, Any], None]:
		while True:
			await asyncio.sleep(0.5)
			# simple dynamics
			if self.motor_status == "forward":
				self.speed = min(100.0, self.speed + 2.5)
			elif self.motor_status == "back":
				self.speed = max(-30.0, self.speed - 2.5)
			else:
				self.speed = self.speed * 0.9
			self.distance_cm = max(5.0, self.distance_cm + random.uniform(-5, 5))
			self.battery_pct = max(0, self.battery_pct - random.choice([0, 0, 1]))
			if self.battery_pct < 15:
				self.led_states["head"] = False

			yield {
				"speed": round(self.speed, 2),
				"distance_cm": round(self.distance_cm, 1),
				"motor_status": self.motor_status,
				"led_states": self.led_states,
				"servo_angle": self.servo_angle,
				"battery_pct": self.battery_pct,
				"drowsy": self.drowsy,
				"emotion": self.emotion,
			}

	async def send_command(self, action: str, value: Optional[Any]) -> bool:
		action = action.lower()
		if action in {"forward", "back", "left", "right", "stop"}:
			if action == "forward":
				self.motor_status = "forward"
			elif action == "back":
				self.motor_status = "back"
			elif action == "left":
				self.servo_angle = max(0, self.servo_angle - 10)
			elif action == "right":
				self.servo_angle = min(180, self.servo_angle + 10)
			elif action == "stop":
				self.motor_status = "stopped"
			return True
		if action.startswith("led_") and isinstance(value, bool):
			key = action.split("_", 1)[1]
			self.led_states[key] = value
			return True
		if action == "set_servo" and isinstance(value, (int, float)):
			self.servo_angle = max(0, min(180, int(value)))
			return True
		return False
