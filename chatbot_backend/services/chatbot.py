import boto3
import uuid
from typing import Dict, Any

AGENT_REGION = "eu-north-1"
AGENT_ID = "3284DGBGLA"
AGENT_ALIAS_ID = "WO4UMEECUC"

try:
    session_chatbot = boto3.Session(profile_name="default")
    bedrock_agent_runtime = session_chatbot.client(
        "bedrock-agent-runtime",
        region_name=AGENT_REGION
    )
except Exception as e:
    print(f"⚠️ Bedrock client initialization failed: {e}")
    bedrock_agent_runtime = None


def invoke_chatbot_agent(user_input: str) -> str:
    """
    Invokes the AWS Bedrock Agent with the user's message.
    """
    if not bedrock_agent_runtime:
        return "Chatbot service is unavailable due to configuration error."

    try:
        session_id = str(uuid.uuid4())
        print(f"💬 Chat started [{session_id}]: {user_input}")

        response = bedrock_agent_runtime.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=session_id,
            inputText=user_input
        )

        event_stream = response.get("completion", [])
        reply = ""

        for event in event_stream:
            if "chunk" in event:
                reply += event["chunk"]["bytes"].decode("utf-8")

        print(f"🧠 Chatbot reply: {reply.strip()}")
        return reply.strip() or "No response received"

    except Exception as e:
        print("❌ Chatbot Error:", str(e))
        raise RuntimeError(f"Chatbot error during invocation: {str(e)}")