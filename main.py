from fastapi import FastAPI, File, UploadFile
import requests
import os
import base64

app = FastAPI()

AI_KEY = os.getenv("AI_KEY")

@app.get("/")
def root():
    return {"status": "SeeBuild AI server running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {AI_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4.1-mini",
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "Analyze this construction image and describe any visible deviations."},
                        {
                            "type": "input_image",
                            "image_base64": image_base64
                        }
                    ]
                }
            ]
        }
    )

    return response.json()
