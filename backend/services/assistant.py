import os
import asyncio
from typing import Optional


class AssistantService:
	def __init__(self) -> None:
		self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
		self.api_key = os.getenv("OPENAI_API_KEY")

	async def chat(self, message: str, language: Optional[str] = "en") -> str:
		if not self.api_key:
			return f"[local] ({language}) You said: {message}"
		# Simulate latency or integrate real model here
		await asyncio.sleep(0.2)
		return f"[simulated-ai] ({language}) Response to: {message}"

	async def voice_chat(self, audio_bytes: bytes, language: Optional[str] = "en") -> dict:
		# Placeholder transcription/AI flow; integrate OpenAI Whisper+Chat if api_key exists
		size_kb = round(len(audio_bytes) / 1024, 1)
		transcript = f"[local transcript] {size_kb} KB audio received"
		answer = await self.chat("User voice message (transcribed)", language=language)
		return {"transcript": transcript, "answer": answer}
