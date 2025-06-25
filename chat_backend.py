from mistralai import Mistral
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=MISTRAL_API_KEY)

@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message", "")

    try:
        response = client.chat.complete(
            model="mistral-small",
            messages=[
                {"role": "system", "content": "أجب باللغة العربية فقط وباختصار، ولا تخترع وظائف."},
                {"role": "user", "content": user_message}
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"response": f"خطأ تقني: {str(e)}"}
