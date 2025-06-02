import psycopg2
import requests
import time

# Vast.ai API ключ
VAST_API_KEY = "your_vast_api_key"

def rent_gpu():
    """Арендуем GPU на Vast.ai"""
    resp = requests.post(
        "https://vast.ai/api/v0/requests/",
        json={"image": "musicgen-worker", "gpu_type": "RTX 4090"},
        headers={"Authorization": f"Bearer {VAST_API_KEY}"}
    )
    return resp.json()["instance_id"]

def check_queue():
    conn = psycopg2.connect("dbname=pgmq user=postgres host=localhost")
    cursor = conn.cursor()
    
    while True:
        # Берём задачу из очереди
        cursor.execute("SELECT pgmq.pop('song_queue')")
        task = cursor.fetchone()
        
        if task:
            task_id, payload = task
            print(f"Processing: {payload['prompt']}")
            
            # Арендуем GPU
            instance_id = rent_gpu()
            
            # Отправляем задачу воркеру (HTTP / WebSocket)
            # В реальности тут будет вызов API воркера
            print(f"Task sent to GPU worker {instance_id}")
            
            # Подтверждаем выполнение
            cursor.execute("SELECT pgmq.ack('song_queue', %s)", (task_id,))
            conn.commit()
        
        time.sleep(1)

if __name__ == "__main__":
    check_queue()