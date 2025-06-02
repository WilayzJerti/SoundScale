import os
import boto3
from musicgen import MusicGen  # Предполагаем, что есть обёртка

# Cloudflare R2
s3 = boto3.client(
    's3',
    endpoint_url=os.getenv("R2_ENDPOINT"),
    aws_access_key_id=os.getenv("R2_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("R2_SECRET_KEY"),
)

def generate_and_upload(prompt: str, duration: int):
    model = MusicGen("facebook/musicgen-small")
    audio = model.generate(prompt, duration)
    
    # Сохраняем в R2
    s3.upload_fileobj(
        audio, "musicgen-bucket", f"tracks/{prompt[:10]}.mp3"
    )
    return f"https://r2.musicgen.cc/tracks/{prompt[:10]}.mp3"

if __name__ == "__main__":
    # В реальности тут будет слушатель RabbitMQ/HTTP
    generate_and_upload("Jazz piano solo", 15)