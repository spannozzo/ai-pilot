from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Define a Pydantic model for input validation
class PromptRequest(BaseModel):
    prompt: str

# Set the Ollama service URL (use the service name defined in Docker Compose)
OLLAMA_SERVICE_URL = "http://ollama:11434/api/generate"  # Adjust 'ollama-service' to your Docker Compose service name

@app.post("/generate")
async def generate_text(request: PromptRequest):
    try:
        # Prepare the payload for Ollama's API
        payload = {
            "model": "llama2", 
            "prompt": request.prompt,
            "stream": False
        }

        # Send the request to the internal Ollama service
        response = requests.post(OLLAMA_SERVICE_URL, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            return {"response": response_data.get("response", "")}
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Ollama service returned an error: {response.text}"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Ollama service: {str(e)}")
