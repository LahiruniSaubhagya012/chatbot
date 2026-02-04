from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.auth import OTPAgent
from services.chatbot import invoke_chatbot_agent
import os
from dotenv import load_dotenv

load_dotenv()

OTP_API_KEY = os.getenv("OTP_API_KEY")

if not OTP_API_KEY:
    print("⚠️ OTP_API_KEY not found in .env. Using hardcoded value.")
    OTP_API_KEY = "atr_3uhYuHqmEk-9N5uaA73nZg"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

otp_agent = OTPAgent(OTP_API_KEY)


# ---------------- OTP ROUTES --------------------------
@app.post("/send-otp")
def send_otp_endpoint(data: dict):
    try:
        phone = data.get("phone_number")
        if not phone:
            raise HTTPException(status_code=400, detail="Phone number required")

        print(f"📞 Received OTP send request for: {phone}")
        response = otp_agent.send_otp(phone)
        print("✅ OTP sent successfully:", response)

        return {"message": "✅ OTP sent successfully", "response": response}
    except RuntimeError as e:
        print("❌ Send OTP Runtime Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print("❌ Send OTP Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal server error during OTP send.")


@app.post("/verify-otp")
def verify_otp_endpoint(data: dict):
    try:
        phone = data.get("phone_number")
        otp = data.get("otp")
        client_secret = data.get("client_secret")  # ✅ added

        if not phone or not otp or not client_secret:
            raise HTTPException(status_code=400, detail="Phone number, OTP, and client_secret required")

        print(f"🧩 Verifying OTP for {phone} with secret {client_secret}")
        response = otp_agent.verify_otp(phone, otp, client_secret)  # ✅ fixed

        print("✅ OTP verification success:", response)
        return {"message": "✅ OTP verified successfully", "response": response}

    except RuntimeError as e:
        print("❌ Verify OTP Runtime Error:", str(e))
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        print("❌ Verify OTP Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal server error during OTP verification.")


# ---------------- CHATBOT ROUTE -----------------------
@app.post("/chat")
def chat_with_agent(data: dict):
    try:
        user_input = data.get("message", "")
        if not user_input:
            raise HTTPException(status_code=400, detail="Message required")

        reply = invoke_chatbot_agent(user_input)
        
        return {"reply": reply}

    except RuntimeError as e:
        print("❌ Chatbot Runtime Error:", str(e))
        raise HTTPException(status_code=503, detail=f"Chatbot service failed: {str(e)}")
    except Exception as e:
        print("❌ General Chatbot Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/")
def health():
    return {"status": "OK", "services": ["Chatbot", "OTP"]}