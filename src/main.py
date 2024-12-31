from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from pydantic import BaseModel
from typing import Optional
import os

from .config import *
from .log_processor import LogProcessor
from .vector_store import VectorStore
from .rag_model import RAGModel

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")


log_processor = LogProcessor(NGINX_LOG_PATH)
vector_store = VectorStore(EMBEDDING_MODEL_NAME, VECTOR_STORE_PATH)
rag_model = RAGModel(LLM_MODEL_NAME, vector_store)

class Question(BaseModel):
    text: str

@app.get("/")
async def root():
    """Ana sayfa için yönlendirme."""
    return {"message": "API çalışıyor. /static/index.html adresine gidin."}

@app.post("/initialize")
async def initialize_system():
    """Sistemi başlatır ve log verilerini işler."""
    try:
        
        logs = log_processor.read_logs()
        if not logs:
            raise HTTPException(status_code=404, detail="Log dosyası bulunamadı veya boş")
            
        
        log_texts = [log_processor.format_log_for_embedding(log) for log in logs]
        
        
        vector_store.create_index(logs, log_texts)
        
        return {"message": "Sistem başarıyla başlatıldı", "log_count": len(logs)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(question: Question):
    """Kullanıcı sorusunu yanıtlar."""
    try:
        
        if not vector_store.load_index():
            raise HTTPException(status_code=400, detail="Sistem henüz başlatılmamış")
                
        
        answer = rag_model.answer_question(question.text)
        return {"answer": answer}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("src.main:app", host=API_HOST, port=API_PORT, reload=True) 