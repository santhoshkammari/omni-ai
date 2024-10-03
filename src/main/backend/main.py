from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from omni_ai import OmniAIChat
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



AVAILABLE_MODELS = ['meta-llama/Meta-Llama-3.1-70B-Instruct',
                               'CohereForAI/c4ai-command-r-plus-08-2024',
                               'Qwen/Qwen2.5-72B-Instruct',
                               'meta-llama/Llama-3.2-11B-Vision-Instruct',
                               'NousResearch/Hermes-3-Llama-3.1-8B',
                               'mistralai/Mistral-Nemo-Instruct-2407',
                               'microsoft/Phi-3.5-mini-instruct'
                               ]
chatbot = OmniAIChat(model=AVAILABLE_MODELS[-1])

class ChatRequest(BaseModel):
    query: str
    web_search: bool = False

@app.post("/api/chat")
async def chat(chat_request: ChatRequest):
    if not chat_request.query:
        raise HTTPException(status_code=400, detail="No query provided")

    def generate():
        try:
            for chunk in chatbot.generator(chat_request.query, web_search=chat_request.web_search):
                yield json.dumps({"content": chunk}) + "\n"
        except Exception as e:
            yield json.dumps({"error": str(e)}) + "\n"

    return StreamingResponse(generate(), media_type="application/json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)