from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Twilio credentials (these should be securely stored, e.g., in environment variables)
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
RECIPIENT_NUMBER = os.getenv("RECIPIENT_NUMBER")

# Pydantic model for the request body
class SMSRequest(BaseModel):
    message_body: str


@app.post("/send-sms/")
async def send_sms(request: SMSRequest):
    try:
        # Create Twilio client
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        # Send SMS
        message = client.messages.create(
            body=request.message_body,
            from_=TWILIO_NUMBER,
            to=RECIPIENT_NUMBER
        )

        return {"message_sid": message.sid, "status": "Message sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI app with Uvicorn
# To run this, save the script as `main.py` and run `uvicorn main:app --reload`
