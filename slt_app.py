import streamlit as st
import boto3
import uuid
import time

# AWS Bedrock Runtime Client 
bedrock_agent_runtime = boto3.client(
    service_name="bedrock-agent-runtime",
    region_name="eu-north-1" 
)

#Agent Config 
AGENT_ID = "3284DGBGLA"
AGENT_ALIAS_ID = "WO4UMEECUC"
SESSION_ID = str(uuid.uuid4()) 

#Page Configuration 
st.set_page_config(
    page_title="SLT Web Portal",
    page_icon="🌐 ",
    layout="wide"
)

#CSS 
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .header {
        background: linear-gradient(135deg, #003366, #005999, #0074C7);
        padding: 15px 0;
        margin-bottom: 20px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .nav-menu {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 15px;
    }
    
    .nav-menu a {
        color: white;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .nav-menu a:hover {
        color: #FFD700;
        transform: translateY(-2px);
    }
                   
    .footer {
        background: linear-gradient(135deg, #003366, #005999);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-top: 30px;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.1);
    }
    
    .footer-content {
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
    }
    
    .chat-container {
        background-color: #E6F7FF;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 20px auto;
        max-width: 800px;
    }
    
    .chat-header {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .stButton button {
        width: 100%;
        background: linear-gradient(to right, #005999, #003366);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: linear-gradient(to right, #003366, #002244);
        transform: translateY(-2px);
    }
    
    .stTextInput input {
        width: 100%;
        border-radius: 8px;
        padding: 12px 15px;
        border: 1px solid #ddd;
    }
    
    .chat-bubble {
        padding: 12px 18px;
        border-radius: 18px;
        margin: 10px 0;
        max-width: 100%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .user-bubble {
        background: linear-gradient(to right, #005999, #0074C7);
        margin-left: auto;
        color: white;
    }
    
    .assistant-bubble {
        background: linear-gradient(to right, #E6F0FF, #D4E5FF);
        margin-right: auto;
        color: #1a1a1a;
    }
    
    .chat-history {
        max-height: 600px;
        overflow-y: auto;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 10px;
        background: #f9f9f9;
    }
            
    </style>
""", unsafe_allow_html=True)

#Header Section
def header():
    st.markdown("""
        <div class="header">
            <div>
                <h1 style="color: #f8f9fa; margin: 0; padding: 5px; text-align: center;">SLT Mobitel</h1>
                <div class="nav-menu">
                    <a href="#">Home</a>
                    <a href="#">Services</a>
                    <a href="#">Packages</a>
                    <a href="#">Support</a>
                    <a href="#">Contact</a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

#Footer Section
def footer():
    st.markdown("""
        <div class="footer">
            <div class="footer-content">
                <div>
                    <p>📞 Customer Service: 1212</p>
                    <p>📧 Email: support@slt.lk</p>
                </div>
                <div>
                    <p>🏢 Headquarters: Lotus Rd, Colombo 1, Sri Lanka</p>
                    <p>© 2025 Sri Lanka Telecom. All Rights Reserved.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

#Chatbot Section
def chatbot_section():
    st.markdown("""
        <div class="chat-container">
            <div class="chat-header">
                <h3 style="color: #003366; margin-bottom: 5px;">🤖 SLT Virtual Assistant</h3>
                <p style="color: #666;">How can I help you?</p>
            </div>
    """, unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    st.markdown('<div class="chat-history">', unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
                <div class="chat-bubble user-bubble">
                    <strong>You:</strong> {message["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-bubble assistant-bubble">
                    <strong>Assistant:</strong> {message["content"]}
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chatbot UI
    user_input = st.text_input("Your question:", placeholder="Ask a question about SLT services...", key="user_input")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Send", key="send_button") and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            st.markdown(f"""
                <div class="chat-bubble user-bubble">
                    <strong>You:</strong> {user_input}
                </div>
            """, unsafe_allow_html=True)
            
            try:
                output_area = st.empty()
                streamed_text = ""

                response = bedrock_agent_runtime.invoke_agent(
                    agentId=AGENT_ID,
                    agentAliasId=AGENT_ALIAS_ID,
                    sessionId=SESSION_ID,
                    inputText=user_input
                )

                for event in response["completion"]:
                    if "chunk" in event:
                        chunk_text = event["chunk"]["bytes"].decode("utf-8")
                        streamed_text += chunk_text
                        output_area.markdown(f"""
                            <div class="chat-bubble assistant-bubble">
                                <strong>Assistant:</strong> {streamed_text}▌
                            </div>
                        """, unsafe_allow_html=True)
                        time.sleep(0.02) 

                output_area.markdown(f"""
                    <div class="chat-bubble assistant-bubble">
                        <strong>Assistant:</strong> {streamed_text}
                    </div>
                """, unsafe_allow_html=True)
                
                st.session_state.messages.append({"role": "assistant", "content": streamed_text})

            except Exception as e:
                error_msg = f"Sorry, I'm experiencing technical difficulties. Please try again later. Error: {str(e)}"
                st.markdown(f"""
                    <div class="chat-bubble assistant-bubble">
                        <strong>Assistant:</strong> {error_msg}
                    </div>
                """, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    st.markdown("</div>", unsafe_allow_html=True)

def main_content():
    chatbot_section()
    
header()
main_content()
footer()