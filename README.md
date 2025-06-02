# SoundScale
This project is a scalable system for generating music using AI. It is designed to remain minimalistic, but easily scalable to high loads (thousands of tracks per day).

### **Key components:**

1. **Customer Application**
    
    - Interface for users to send music generation requests over HTTPS.
        
2. **API server (FastAPI on Fly.io)**
    
    - Receives requests from the client, validates them and queues them (PGMQ).
        
3. **Task Queue (PGMQ on Postgres)**
    
    - Stores track generation tasks.
        
    - PGMQ is a lightweight PostgreSQL-based queue, making it easy to manage tasks without a separate broker (like RabbitMQ).
        
4. **Orchestrator (Fly.io)**.
    
    - Picks up tasks from the queue and manages **renting GPU nodes** via **Vast.ai** (analogous to AWS EC2, but cheaper).
        
    - Sends tasks to free wokers.
        
5. **SongWorker (GPU on Vast.ai, e.g. RTX 4090)**
    
    - Runs **MusicGen** (+ LoRA for style customization).
        
    - Uploads finished tracks to **Cloudflare R2** (analogous to S3, but with cheap egress traffic).
        
6. **Storage (Cloudflare R2)**.
    
    - Cloud storage for generated tracks.
        

### **Architectural Features:**

- **Autoscaling:**
    
    - Orchestrator dynamically rents GPUs on Vast.ai under load and frees them when tasks are finished.
        
- **Economy:**
    
    - Low-cost services (Fly.io, Vast.ai, Cloudflare R2) are used.
        
- **Minimalism:**
    
    - All queue and task logic is inside PostgreSQL, without unnecessary dependencies.

Translated with DeepL.com (free version)
