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
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://mongocontainer:27017/mydb")
REDIS_URL = os.getenv("REDIS_URL", "redis://rediscontainer:6379")
print(f"Starting FastAPI backend...")
print(f"Using MONGODB_URL: {MONGODB_URL}")
print(f"Using REDIS_URL: {REDIS_URL}")

# Initialize clients
try:
      mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
      print("connection mongo - Successfully initialized MongoDB client")
except Exception as e:
    print("error initializing MongoDB client:", e)

db = mongo_client["mydatabase"]

try:
     redis_client = redis.from_url(REDIS_URL, decode_responses=True)
     print("connection redis - Successfully initialized Redis client")
except Exception as e:
     print("redis error:", e)

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
