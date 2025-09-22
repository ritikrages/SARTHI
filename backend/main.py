from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import os
from typing import List, Optional, Dict, Any

from services.telemetry_manager import TelemetryManager
from services.assistant import AssistantService
from services.alerts import AlertsService
from services.vision import VisionService


class ControlCommand(BaseModel):
	action: str
	value: Optional[Any] = None


class ChatRequest(BaseModel):
	message: str
	language: Optional[str] = "en"


class Esp32Payload(BaseModel):
	device_id: str
	temperature: Optional[float] = None
	humidity: Optional[float] = None
	alcohol_ppm: Optional[float] = None
	heart_rate_bpm: Optional[float] = None
	steering_grip: Optional[float] = None
	posture_score: Optional[float] = None
	vehicle_state: Optional[str] = None
	ultrasonic_dist: Optional[int] = None
	alert_active: Optional[bool] = None
	raw_data: Optional[Dict[str, Any]] = None


app = FastAPI(title="Vehicle Monitor Backend", version="0.1.0")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

telemetry_manager = TelemetryManager()
assistant_service = AssistantService()
alerts_service = AlertsService()
vision_service = VisionService()


connections: List[WebSocket] = []


@app.on_event("startup")
async def on_startup() -> None:
	asyncio.create_task(telemetry_manager.run())
	asyncio.create_task(broadcast_telemetry_loop())
	# vision service can be started on demand


@app.get("/api/health")
async def health() -> Dict[str, Any]:
	return {"status": "ok"}


@app.get("/api/telemetry/latest")
async def get_latest() -> Dict[str, Any]:
	return telemetry_manager.get_latest()


@app.post("/api/control/command")
async def send_command(cmd: ControlCommand) -> Dict[str, Any]:
	ok = await telemetry_manager.send_command(cmd.action, cmd.value)
	return {"ok": ok}


@app.post("/api/assistant/chat")
async def chat(req: ChatRequest) -> Dict[str, Any]:
	answer = await assistant_service.chat(req.message, language=req.language)
	return {"answer": answer}


@app.post("/api/assistant/voice")
async def voice(file: UploadFile = File(...), language: str = Form("en")) -> Dict[str, Any]:
	data = await file.read()
	resp = await assistant_service.voice_chat(data, language=language)
	return resp


@app.get("/api/alerts/history")
async def get_alerts_history() -> Dict[str, Any]:
	return {"items": alerts_service.history()}


@app.post("/api/alerts/test")
async def test_alert(background_tasks: BackgroundTasks) -> Dict[str, Any]:
	background_tasks.add_task(alerts_service.send_sos, reason="test", details={"ts": asyncio.get_event_loop().time()})
	return {"queued": True}


@app.post("/api/vision/toggle")
async def toggle_vision(enabled: bool) -> Dict[str, Any]:
	vision_service.enabled = enabled
	if enabled and not vision_service.is_running:
		asyncio.create_task(vision_service.run(telemetry_manager, alerts_service))
	return {"enabled": vision_service.enabled}


# ---------- ESP32 Integration ----------
@app.get("/esp32/config/{device_id}")
async def get_esp32_config(device_id: str) -> Dict[str, Any]:
	return {
		"device_id": device_id,
		"sampling_rate": int(os.getenv("ESP32_SAMPLING_MS", "2000")),
		"alcohol_threshold": float(os.getenv("ESP32_ALCOHOL_THRESHOLD", "0.02")),
	}


@app.post("/esp32/sensor-data")
async def ingest_esp32(payload: Esp32Payload, background_tasks: BackgroundTasks) -> Dict[str, Any]:
	mapped: Dict[str, Any] = {
		"speed": telemetry_manager.get_latest().get("speed", 0),
		"distance_cm": payload.ultrasonic_dist,
		"motor_status": payload.vehicle_state or "unknown",
		"led_states": telemetry_manager.get_latest().get("led_states", {"left": False, "right": False, "head": True}),
		"servo_angle": telemetry_manager.get_latest().get("servo_angle", 90),
		"battery_pct": telemetry_manager.get_latest().get("battery_pct", 80),
		"drowsy": telemetry_manager.get_latest().get("drowsy", False),
		"emotion": telemetry_manager.get_latest().get("emotion", "neutral"),
		"temperature": payload.temperature,
		"humidity": payload.humidity,
		"alcohol_ppm": payload.alcohol_ppm,
		"heart_rate_bpm": payload.heart_rate_bpm,
		"steering_grip": payload.steering_grip,
		"posture_score": payload.posture_score,
		"device_id": payload.device_id,
	}
	await telemetry_manager.update_external(mapped)
	# Trigger SOS if alert flag raised or alcohol threshold exceeded
	threshold = float(os.getenv("ESP32_ALCOHOL_THRESHOLD", "0.02"))
	if (payload.alert_active is True) or (payload.alcohol_ppm is not None and payload.alcohol_ppm >= threshold):
		background_tasks.add_task(alerts_service.send_sos, reason="esp32_alert", details=mapped)
	return {"ok": True}


@app.websocket("/ws/telemetry")
async def websocket_endpoint(ws: WebSocket) -> None:
	await ws.accept()
	connections.append(ws)
	try:
		while True:
			await asyncio.sleep(5)
			# keep alive
	except WebSocketDisconnect:
		pass
	finally:
		if ws in connections:
			connections.remove(ws)


async def broadcast_telemetry_loop() -> None:
	while True:
		await asyncio.sleep(0.5)
		data = telemetry_manager.get_latest()
		if not data:
			continue
		to_remove: List[WebSocket] = []
		for ws in connections:
			try:
				await ws.send_json({"type": "telemetry", "data": data})
			except Exception:
				to_remove.append(ws)
		for ws in to_remove:
			if ws in connections:
				connections.remove(ws)


if __name__ == "__main__":
	import uvicorn
	uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
