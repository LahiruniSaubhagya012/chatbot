import requests
import time
from typing import Dict, Any

SEND_OTP_URL = "http://emy.raccoon-ai.com:8000/api/v1/sms/send-otp"
VERIFY_OTP_URL = "http://emy.raccoon-ai.com:8000/api/v1/sms/verify-otp"

class OTPAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def _format_phone_number(self, phone_number: str) -> str:
        """Convert phone number to local format (07********)"""
        cleaned = phone_number.replace(" ", "").replace("-", "").replace("+", "")
        
        if cleaned.startswith("94"):
            return "0" + cleaned[2:]  
        
        if cleaned.startswith("94"):
            return "0" + cleaned[2:]
       
        if cleaned.startswith("07"):
            return cleaned
      
        if len(cleaned) == 9 and cleaned.startswith("7"):
            return "0" + cleaned
       
        return cleaned

    def send_otp(self, phone_number: str) -> Dict[str, Any]:
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
       
        formatted_number = self._format_phone_number(phone_number)
        
        payload = {
            "mobile": formatted_number,
        }

        try:
            print(f"📨 Sending OTP to {formatted_number} (original: {phone_number})")
            res = requests.post(SEND_OTP_URL, headers=headers, json=payload, timeout=30)
            print("🔹 OTP Response Code:", res.status_code)
            print("🔹 OTP Response:", res.text)

            res.raise_for_status()
            return res.json()

        except requests.HTTPError as e:
            try:
                err_detail = e.response.json()
            except Exception:
                err_detail = e.response.text
            raise RuntimeError(f"OTP send failed ({e.response.status_code}): {err_detail}")
        except Exception as e:
            raise RuntimeError(f"Failed to send OTP: {str(e)}")

    def verify_otp(self, phone_number: str, otp: str, client_secret: str) -> Dict[str, Any]:
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        formatted_number = self._format_phone_number(phone_number)
        
        payload = {
            "mobile": formatted_number,
            "otp": otp,
            "client_secret": client_secret  
        }

        try:
            print(f"🔍 Verifying OTP for {formatted_number} (original: {phone_number})...")
            res = requests.post(VERIFY_OTP_URL, headers=headers, json=payload, timeout=30)
            print("🔹 Verify Response Code:", res.status_code)
            print("🔹 Verify Response:", res.text)

            res.raise_for_status()
            return res.json()

        except requests.HTTPError as e:
            try:
                err_detail = e.response.json()
            except Exception:
                err_detail = e.response.text
            raise RuntimeError(f"OTP verify failed ({e.response.status_code}): {err_detail}")
        except Exception as e:
            raise RuntimeError(f"Failed to verify OTP: {str(e)}")