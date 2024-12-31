import sqlite3
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
import json
import os

class VectorStore:
    def __init__(self, model_name: str, vector_store_path: str):
        self.model = SentenceTransformer(model_name)
        self.db_path = os.path.join(vector_store_path, 'vectors.db')
        os.makedirs(vector_store_path, exist_ok=True)
        
    def get_connection(self):
        """Her sorgu için yeni bir bağlantı oluşturur."""
        return sqlite3.connect(self.db_path)
        
    def create_tables(self, conn):
        """Gerekli tabloları oluşturur."""
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY,
                    log_data TEXT,
                    embedding BLOB,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
    def create_index(self, logs: List[Dict], log_texts: List[str]):
        """Loglar için vektör indeksi oluşturur."""
        conn = self.get_connection()
        self.create_tables(conn)
        
        
        with conn:
            conn.execute('DELETE FROM logs')
        
        
        embeddings = self.model.encode(log_texts)
        
        with conn:
            for i, (log, embedding) in enumerate(zip(logs, embeddings)):
                conn.execute(
                    'INSERT INTO logs (log_data, embedding) VALUES (?, ?)',
                    (json.dumps(log), embedding.tobytes())
                )
        
        conn.close()
                
    def load_index(self):
        """Veritabanının varlığını kontrol eder."""
        return os.path.exists(self.db_path)
            
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Verilen sorgu için en yakın k log kaydını döndürür."""
        conn = self.get_connection()
        query_vector = self.model.encode([query])[0]
        
       
        cursor = conn.execute('SELECT log_data, embedding FROM logs')
        results = []
        
        for log_data, embedding_bytes in cursor:
            embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
            similarity = np.dot(query_vector, embedding) / (np.linalg.norm(query_vector) * np.linalg.norm(embedding))
            results.append((similarity, json.loads(log_data)))
        
        conn.close()
        
      
        results.sort(key=lambda x: x[0], reverse=True)
        return [log for _, log in results[:k]] 