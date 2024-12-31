import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


NGINX_LOG_PATH = "C:/nginx/logs/access.log"


VECTOR_STORE_PATH = os.path.join(BASE_DIR, 'vector_store')


EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_NAME = "google/flan-t5-base"  


API_HOST = "localhost"
API_PORT = 8000 