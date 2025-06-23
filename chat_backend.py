from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# السماح لأي موقع يتواصل مع السيرفر (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


openai.api_key = os.getenv("OPENAI_API_KEY")


@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أجب على الأسئلة باللغة العربية وباختصار، ولا تخترع وظائف."},
                {"role": "user", "content": user_message}
            ]
        )
        return {"response": response.choices[0].message["content"]}
    except Exception as e:
        return {"response": f"خطأ تقني: {str(e)}"}
