import streamlit as st
import boto3
import uuid
import time
import json

REGION = "eu-north-1"
AGENT_ID = "3284DGBGLA"
AGENT_ALIAS_ID = "WO4UMEECUC"
SESSION_ID = str(uuid.uuid4())
LAMBDA_FUNCTION_NAME = "sent_otp-s3a4r"

bedrock_agent_runtime = boto3.client("bedrock-agent-runtime", region_name=REGION)
lambda_client = boto3.client("lambda", region_name=REGION)

def send_otp(phone_number):
    """Invoke Lambda to send OTP and return it."""
    payload = {"phone_number": phone_number}
    response = lambda_client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload)
    )
    raw_payload = response["Payload"].read().decode("utf-8")
    result = json.loads(raw_payload)
    body = json.loads(result["body"])
    return body["otp"]

st.set_page_config(page_title="SLT Web Portal", page_icon="🌐", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    header[data-testid="stHeader"] {display: none;}
    footer {visibility: hidden;}
    div.block-container {padding-top: 1rem; padding-bottom: 1rem;}
    html, body, [data-testid="stAppViewContainer"] {
        font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background: linear-gradient(135deg, #f0f4f8, #e0e8f0);
    }
    .login-card {
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        max-width: 500px;
        margin: 50px auto;
        text-align: center;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

def header():
    st.markdown("""
        <div style="background: linear-gradient(135deg, #007bff, #0056b3); padding: 25px; color: white; text-align:center; font-size: 32px; font-weight:700; border-radius:0 0 20px 20px;">
            SLT MOBITEL Virtual Assistant 🤖
        </div>
    """, unsafe_allow_html=True)

def footer():
    st.markdown("""
        <div style="background:#343a40; color:white; padding:15px; text-align:center; border-radius:20px 20px 0 0;">
            © 2025 Sri Lanka Telecom. All Rights Reserved.
        </div>
    """, unsafe_allow_html=True)

def chatbot_section():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your SLT Mobitel virtual assistant. How can I help you today? 💬"}
        ]
    for message in st.session_state.messages:
        role_class = "user" if message["role"] == "user" else "assistant"
        bg = "#007bff" if role_class == "user" else "#ffffff"
        color = "#fff" if role_class == "user" else "#333"
        align = "right" if role_class == "user" else "left"
        st.markdown(
            f"<div style='background:{bg};color:{color};padding:12px;border-radius:15px;margin:8px;text-align:{align};max-width:80%;margin-{('left' if role_class=='user' else 'right')}:auto;'>{message['content']}</div>",
            unsafe_allow_html=True
        )

    user_input = st.text_input("💬 Type your message here", key="user_input")
    if st.button("Send ➤") and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})
        try:
            response = bedrock_agent_runtime.invoke_agent(
                agentId=AGENT_ID,
                agentAliasId=AGENT_ALIAS_ID,
                sessionId=SESSION_ID,
                inputText=user_input
            )
            streamed_text = ""
            for event in response["completion"]:
                if "chunk" in event:
                    streamed_text += event["chunk"]["bytes"].decode("utf-8")
            st.session_state.messages.append({"role": "assistant", "content": streamed_text})
            st.rerun()
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"⚠️ Error: {e}"})
            st.rerun()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='color:#007bff;'>🔐 SLT Web Portal Login</h2>", unsafe_allow_html=True)

    phone_number = st.text_input("Enter your mobile number (e.g., +947XXXXXXXX)", placeholder="Mobile Number")

    if st.button("Send OTP", use_container_width=True):
        if phone_number:
            try:
                with st.spinner('Sending OTP...'):
                    otp = send_otp(phone_number)
                    st.session_state.generated_otp = otp

                st.success("✅ OTP sent successfully to your number!")
                st.info(f"(Testing only) OTP: {otp}")

            except Exception as e:
                st.error(f"Failed to send OTP: {e}")
        else:
            st.warning("Please enter a valid phone number.")

    if "generated_otp" in st.session_state:
        entered_otp = st.text_input("Enter the OTP you received", placeholder="6-digit OTP")
        if st.button("Verify OTP", use_container_width=True):
            if entered_otp == st.session_state.generated_otp:
                st.session_state.authenticated = True
                st.success("✅ Verification successful! Welcome to the portal.")
                st.rerun()
            else:
                st.error("❌ Incorrect OTP. Please try again.")

    st.markdown('</div>', unsafe_allow_html=True)

else:
    header()
    chatbot_section()
    footer()
