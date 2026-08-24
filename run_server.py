import uvicorn
from api_server import app
from database import init_db

if __name__ == "__main__":
    init_db()
    print("🚀 Starting TikTok Trend Intelligence API on port 8001...")
    print("📚 API Documentation: http://localhost:8001/docs")
    print("🔍 Health Check: http://localhost:8001/api/health")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
