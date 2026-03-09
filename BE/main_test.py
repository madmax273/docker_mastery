from fastapi import FastAPI
import os
import motor.motor_asyncio
import redis.asyncio as redis
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get environment variables with fallback defaults for local loose running
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
print(f"Starting FastAPI backend...")
print(f"Using MONGODB_URL: {MONGODB_URL}")
print(f"Using REDIS_URL: {REDIS_URL}")

# Initialize clients
mongo_client = None
db = None
redis_client = None


@app.get("/")
def read_root():
    print("Root endpoint '/' called")
    return {"message": "Hello from FastAPI backend"}

@app.get("/health")
async def health_check():
    print("Health check endpoint '/health' called")
    # Check MongoDB
    try:
        await db.command("ping")
        mongo_status = "connected"
    except Exception as e:
        mongo_status = f"failed: {e}"

    # Check Redis
    try:
        await redis_client.ping()
        redis_status = "connected"
    except Exception as e:
        redis_status = f"failed: {e}"

    return {
        "mongodb": mongo_status,
        "redis": redis_status
    }
