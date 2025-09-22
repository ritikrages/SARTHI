import os
import smtplib
from email.mime.text import MIMEText
from typing import Dict, Any, List
from datetime import datetime


class AlertsService:
	def __init__(self) -> None:
		self.twilio_sid = os.getenv("TWILIO_SID")
		self.twilio_token = os.getenv("TWILIO_TOKEN")
		self.twilio_from = os.getenv("TWILIO_FROM")
		self.twilio_to = os.getenv("TWILIO_TO")
		self.smtp_host = os.getenv("SMTP_HOST")
		self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
		self.smtp_user = os.getenv("SMTP_USER")
		self.smtp_pass = os.getenv("SMTP_PASS")
		self.smtp_to = os.getenv("ALERT_EMAIL_TO")
		self._history: List[Dict[str, Any]] = []

	def send_sos(self, reason: str, details: Dict[str, Any]) -> None:
		record = {
			"ts": datetime.utcnow().isoformat() + "Z",
			"reason": reason,
			"details": details,
		}
		self._history.append(record)
		text = f"SOS Triggered: {reason}\nDetails: {details}"
		# Email first (works offline with local SMTP relay if available)
		if self.smtp_host and self.smtp_to:
			msg = MIMEText(text)
			msg["Subject"] = f"SOS Alert: {reason}"
			msg["From"] = self.smtp_user or "alerts@example.com"
			msg["To"] = self.smtp_to
			with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
				server.starttls()
				if self.smtp_user and self.smtp_pass:
					server.login(self.smtp_user, self.smtp_pass)
				server.send_message(msg)
		# Twilio SMS (optional)
		if self.twilio_sid and self.twilio_token and self.twilio_from and self.twilio_to:
			try:
				from twilio.rest import Client
				client = Client(self.twilio_sid, self.twilio_token)
				client.messages.create(body=text, from_=self.twilio_from, to=self.twilio_to)
			except Exception:
				pass

	def history(self) -> List[Dict[str, Any]]:
		return list(self._history[-200:])
