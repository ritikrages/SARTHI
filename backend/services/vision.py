import asyncio
from typing import Optional, Any
from collections import deque

try:
	import cv2
	import mediapipe as mp
except Exception:
	cv2 = None
	mp = None


class VisionService:
	def __init__(self) -> None:
		self.enabled = False
		self.is_running = False
		self.camera_index = 0
		self.ear_threshold = 0.21  # eye aspect ratio threshold
		self.mar_threshold = 0.65  # mouth aspect ratio threshold for yawn
		self.consec_drowsy_frames = 8
		self._drowsy_counter = 0
		self._last_emotion = "neutral"

	async def run(self, telemetry_manager: Any, alerts_service: Any) -> None:
		if self.is_running:
			return
		self.is_running = True
		self.enabled = True
		cap = None
		facemesh = None
		if cv2 is not None and mp is not None:
			cap = cv2.VideoCapture(self.camera_index)
			facemesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)
		try:
			while self.enabled:
				await asyncio.sleep(0)
				if cap is None or facemesh is None:
					await asyncio.sleep(0.2)
					continue
				ok, frame = cap.read()
				if not ok:
					await asyncio.sleep(0.05)
					continue
				rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				res = facemesh.process(rgb)
				updated = {}
				if res.multi_face_landmarks:
					lm = res.multi_face_landmarks[0]
					pts = [(p.x, p.y) for p in lm.landmark]
					# Indices: using MediaPipe FaceMesh landmarks for eyes and mouth
					# Left eye (example indices)
					LE = [33, 246, 161, 160, 159, 158, 157, 173]
					RE = [263, 466, 388, 387, 386, 385, 384, 398]
					# Mouth
					MOUTH = [13, 14, 78, 308]
					def euclid(a, b):
						ax, ay = a
						bx, by = b
						return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5
					def eye_aspect(indices):
						# rough EAR: vertical/ horizontal using two vertical pairs and one horizontal
						p = pts
						v1 = euclid(p[indices[3]], p[indices[1]])
						v2 = euclid(p[indices[4]], p[indices[2]])
						h = euclid(p[indices[0]], p[indices[5]])
						if h == 0:
							return 0.0
						return (v1 + v2) / (2.0 * h)
					left_ear = eye_aspect(LE)
					right_ear = eye_aspect(RE)
					ear = (left_ear + right_ear) / 2.0
					# Mouth aspect ratio: vertical/horizontal roughly using top/bottom and corners
					mar = 0.0
					try:
						mar_v = euclid(pts[MOUTH[0]], pts[MOUTH[1]])
						mar_h = euclid(pts[MOUTH[2]], pts[MOUTH[3]])
						mar = mar_v / max(mar_h, 1e-6)
					except Exception:
						mar = 0.0
					# Drowsiness logic
					if ear < self.ear_threshold:
						self._drowsy_counter += 1
					else:
						self._drowsy_counter = 0
					is_drowsy = self._drowsy_counter >= self.consec_drowsy_frames or (mar >= self.mar_threshold)
					updated["drowsy"] = is_drowsy
					# Emotion very simple heuristic: yawn -> tired
					emotion = "tired" if mar >= self.mar_threshold else "neutral"
					updated["emotion"] = emotion
					await telemetry_manager.update_external(updated)
					if is_drowsy:
						alerts_service.send_sos("drowsiness", {"ear": round(ear,3), "mar": round(mar,3)})
				else:
					await asyncio.sleep(0.05)
		finally:
			self.is_running = False
			if cap is not None:
				cap.release()
