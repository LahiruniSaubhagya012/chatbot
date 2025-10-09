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

# AWS Clients
bedrock_agent_runtime = boto3.client("bedrock-agent-runtime", region_name=REGION)
lambda_client = boto3.client("lambda", region_name=REGION)

def send_otp(phone_number):
    """Invoke the Lambda function to send an OTP."""
    payload = {"phone_number": phone_number}

    response = lambda_client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload)
    )

    raw_payload = response["Payload"].read().decode("utf-8")

    print("Lambda Raw Response:", raw_payload)

    result = json.loads(raw_payload)
    body = json.loads(result["body"])
    return body["otp"]

st.set_page_config(
    page_title="SLT Web Portal",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>

    header[data-testid="stHeader"] {display: none;}
    footer {visibility: hidden;}
    div.block-container {
        padding-top: 1rem; 
        padding-bottom: 1rem;
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
        background: linear-gradient(135deg, #f0f4f8, #e0e8f0); 
    }
    
    .stTextInput>div>div>input, .stButton>button {
        border-radius: 12px;
        border: 1px solid #ced4da;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stButton>button {
        background-color: #007bff; 
        color: white;
        font-weight: bold;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .user-message {
        background: #007bff; 
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        text-align: right;
        max-width: 85%;
        margin-left: auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .assistant-message {
        background: #ffffff; 
        color: #333333;
        padding: 12px 18px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        text-align: left;
        max-width: 85%;
        margin-right: auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
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

    .stTextInput, .stButton {
        z-index: 100; 
    }

    </style>
""", unsafe_allow_html=True)

def header():
    st.markdown("""
        <div style="background: linear-gradient(135deg, #007bff, #0056b3); padding: 25px; color: white; text-align:center; font-size: 32px; font-weight:700; border-radius:0 0 20px 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
            <span style="letter-spacing: 2px;">SLT MOBITEL</span> Virtual Assistant 🤖
        </div>
    """, unsafe_allow_html=True)

def footer():
    st.markdown("""
        <div style="background:#343a40; color:white; padding:15px; text-align:center; border-radius:20px 20px 0 0; margin-top: 20px;">
            © 2025 Sri Lanka Telecom. All Rights Reserved.
        </div>
    """, unsafe_allow_html=True)

def chatbot_section():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your **SLT Mobitel** virtual assistant. I can help with services, packages, and support. How can I assist you today? 💡"}
        ]

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistant-message'>{message['content']}</div>", unsafe_allow_html=True)

    with st.form(key='chat_form', clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            user_input = st.text_input("💬 Type your message", key="user_input", placeholder="Ask about services, packages, or support...", label_visibility="collapsed")
        with col2:
            send_button = st.form_submit_button("Send ➤")

    if send_button and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})
     
        st.rerun() 

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":

        try:
            response_placeholder = st.empty()
            streamed_text = ""
            
            response = bedrock_agent_runtime.invoke_agent(
                agentId=AGENT_ID,
                agentAliasId=AGENT_ALIAS_ID,
                sessionId=SESSION_ID,
                inputText=st.session_state.messages[-1]["content"] # Use the most recent message
            )
            
            for event in response["completion"]:
                if "chunk" in event:
                    chunk_text = event["chunk"]["bytes"].decode("utf-8")
                    streamed_text += chunk_text
                    
                    temp_html = f"<div class='assistant-message'>{streamed_text} **|**</div>" # Add a cursor
                    response_placeholder.markdown(temp_html, unsafe_allow_html=True)
                    time.sleep(0.03)

            final_html = f"<div class='assistant-message'>{streamed_text}</div>"
            response_placeholder.markdown(final_html, unsafe_allow_html=True)
            
            st.session_state.messages.append({"role": "assistant", "content": streamed_text})
            
        except Exception as e:
            error_msg = f"⚠️ **Error:** Could not connect to the assistant. Please try again. ({e})"
            error_html = f"<div class='assistant-message' style='background:#fde8e8; color:#a31621;'>{error_msg}</div>"
            st.markdown(error_html, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='color: #007bff; margin-bottom: 20px;'>🔐 SLT Web Portal Login</h2>", unsafe_allow_html=True)
    
    phone_number = st.text_input("Enter your mobile number (e.g., +947XXXXXXXX)", placeholder="Mobile Number")

    if st.button("Send OTP", use_container_width=True, key="send_otp_btn"):
        if phone_number:
            try:
                with st.spinner('Sending OTP...'):
                    st.session_state.generated_otp = send_otp(phone_number)
                st.success("📲 OTP sent successfully! Please check your phone.")
            except Exception as e:
                st.error(f"Failed to send OTP. Please check the number and try again.")

        else:
            st.warning("Please enter a valid phone number.")

    if "generated_otp" in st.session_state:
        st.divider() 
        entered_otp = st.text_input("Enter the OTP you received", placeholder="6-digit OTP")

        if st.button("Verify OTP", use_container_width=True, key="verify_otp_btn"):
            if entered_otp == st.session_state.generated_otp:
                st.session_state.authenticated = True
                st.success("✅ Verification successful! Welcome to the portal.")
                st.rerun()
            else:
                st.error("❌ Incorrect OTP. Please try again.")

    st.markdown('</div>', unsafe_allow_html=True)

else:
    header()
    st.container()
    chatbot_section()
    footer() 
