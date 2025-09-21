from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from google.genai import Client

app = Flask(__name__)


client = Client(api_key="AIzaSyAsdnyAvxYOwbxyKtDF3lT0f8cy7OhP5rQ")  

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    
    user_msg = request.form.get("Body")

    
    system_prompt = (
        "You are a medical assistant AI. Only answer questions related to health, "
        "medicines, treatments, symptoms, and wellness. Do not answer unrelated topics."
    )

    
    try:
        gemini_resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{system_prompt}\nUser: {user_msg}\nAI:"
        )
        answer = gemini_resp.text.strip()
    except Exception:
        answer = "Sorry, I could not understand your question. Please ask about health or medicines."

    
    twilio_resp = MessagingResponse()
    twilio_resp.message(answer)
    return str(twilio_resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
