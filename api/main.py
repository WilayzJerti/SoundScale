from fastapi import FastAPI, HTTPException
import psycopg2
from pydantic import BaseModel

app = FastAPI()

# Подключение к PGMQ (Postgres)
conn = psycopg2.connect("dbname=pgmq user=postgres host=localhost")
cursor = conn.cursor()

class SongRequest(BaseModel):
    prompt: str
    duration: int = 10  # секунд

@app.post("/generate")
async def generate_song(request: SongRequest):
    # Добавляем задачу в очередь
    cursor.execute(
        "SELECT pgmq.send('song_queue', %s::jsonb)",
        ({"prompt": request.prompt, "duration": request.duration},)
    )
    conn.commit()
    return {"status": "queued", "message": "Song generation started."}