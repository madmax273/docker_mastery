import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os

# Add parent directory to path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from FastAPI backend"}


@pytest.mark.asyncio
async def test_health_check_success():
    """Test health check when both MongoDB and Redis are connected"""
    with patch('main.db') as mock_db, \
         patch('main.redis_client') as mock_redis:
        
        # Mock successful ping responses
        mock_db.command = AsyncMock(return_value={"ok": 1})
        mock_redis.ping = AsyncMock(return_value=True)
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["mongodb"] == "connected"
        assert data["redis"] == "connected"


@pytest.mark.asyncio
async def test_health_check_mongodb_failure():
    """Test health check when MongoDB fails"""
    with patch('main.db') as mock_db, \
         patch('main.redis_client') as mock_redis:
        
        # Mock MongoDB failure and Redis success
        mock_db.command = AsyncMock(side_effect=Exception("Connection failed"))
        mock_redis.ping = AsyncMock(return_value=True)
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "failed" in data["mongodb"]
        assert data["redis"] == "connected"


@pytest.mark.asyncio
async def test_health_check_redis_failure():
    """Test health check when Redis fails"""
    with patch('main.db') as mock_db, \
         patch('main.redis_client') as mock_redis:
        
        # Mock MongoDB success and Redis failure
        mock_db.command = AsyncMock(return_value={"ok": 1})
        mock_redis.ping = AsyncMock(side_effect=Exception("Connection failed"))
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["mongodb"] == "connected"
        assert "failed" in data["redis"]


@pytest.mark.asyncio
async def test_health_check_both_fail():
    """Test health check when both MongoDB and Redis fail"""
    with patch('main.db') as mock_db, \
         patch('main.redis_client') as mock_redis:
        
        # Mock both failures
        mock_db.command = AsyncMock(side_effect=Exception("Mongo error"))
        mock_redis.ping = AsyncMock(side_effect=Exception("Redis error"))
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "failed" in data["mongodb"]
        assert "failed" in data["redis"]


def test_cors_middleware():
    """Test that CORS middleware is properly configured"""
    # Check if CORS middleware is in the app middleware stack
    from fastapi.middleware.cors import CORSMiddleware
    cors_middleware = None
    for middleware in app.user_middleware:
        if middleware.cls == CORSMiddleware:
            cors_middleware = middleware
            break
    
    assert cors_middleware is not None, "CORS middleware not found"
