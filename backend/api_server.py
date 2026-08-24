from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy import func

from database import SessionLocal, init_db, Trend, UserProfile
from seed_data import seed_data

app = FastAPI(
    title="TikTok Trend Intelligence API",
    description="AI-powered trend detection for TikTok creators",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserProfileCreate(BaseModel):
    username: str
    niche: str
    follower_count: int = 0
    engagement_rate: float = 0.05
    goals: List[str] = []

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {
        "message": "TikTok Trend Intelligence API",
        "version": "1.0.0",
        "endpoints": [
            "/api/trends/current",
            "/api/stats/overview",
            "/api/user/create",
            "/api/user/{id}/opportunities"
        ]
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/api/trends/current")
async def get_current_trends(db=Depends(get_db)):
    try:
        trends = db.query(Trend).filter(
            Trend.expires_at > datetime.utcnow()
        ).order_by(Trend.trend_score.desc()).all()
        
        return [
            {
                "id": t.id,
                "type": t.trend_type,
                "name": t.trend_name,
                "trend_score": t.trend_score,
                "growth_rate": t.growth_rate,
                "competition_level": t.competition_level,
                "trend_stage": t.trend_stage,
                "video_count": t.video_count,
                "engagement_rate": t.engagement_rate
            }
            for t in trends
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats/overview")
async def get_stats(db=Depends(get_db)):
    try:
        total_trends = db.query(Trend).count()
        active_trends = db.query(Trend).filter(
            Trend.expires_at > datetime.utcnow()
        ).count()
        
        top_trend = db.query(Trend).order_by(Trend.trend_score.desc()).first()
        avg_growth = db.query(func.avg(Trend.growth_rate)).scalar() or 0
        
        return {
            "total_trends": total_trends,
            "active_trends": active_trends,
            "average_growth_rate": round(avg_growth, 2),
            "top_trend": {
                "name": top_trend.trend_name if top_trend else "N/A",
                "score": top_trend.trend_score if top_trend else 0
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user/create")
async def create_user(profile: UserProfileCreate, db=Depends(get_db)):
    try:
        existing = db.query(UserProfile).filter_by(
            username=profile.username
        ).first()
        
        if existing:
            existing.niche = profile.niche
            existing.follower_count = profile.follower_count
            existing.engagement_rate = profile.engagement_rate
            existing.goals = profile.goals
            user = existing
        else:
            user = UserProfile(
                username=profile.username,
                niche=profile.niche,
                follower_count=profile.follower_count,
                engagement_rate=profile.engagement_rate,
                goals=profile.goals
            )
            db.add(user)
        
        db.commit()
        db.refresh(user)
        
        return {"id": user.id, "message": "Profile created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/{user_id}/opportunities")
async def get_opportunities(user_id: int, db=Depends(get_db)):
    try:
        user = db.query(UserProfile).filter_by(id=user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        trends = db.query(Trend).filter(
            Trend.expires_at > datetime.utcnow()
        ).order_by(Trend.trend_score.desc()).all()
        
        opportunities = []
        for trend in trends:
            # Simple compatibility calculation
            trend_name = trend.trend_name.lower()
            user_niche = user.niche.lower()
            
            compatibility = 50  # Default
            if user_niche in trend_name:
                compatibility = 90
            elif any(interest in trend_name for interest in user.interests if user.interests):
                compatibility = 75
            
            if compatibility >= 50:
                opportunities.append({
                    "id": trend.id,
                    "name": trend.trend_name,
                    "type": trend.trend_type,
                    "trend_score": trend.trend_score,
                    "growth_rate": trend.growth_rate,
                    "competition_level": trend.competition_level,
                    "trend_stage": trend.trend_stage,
                    "compatibility_score": compatibility,
                    "opportunity_score": round(trend.trend_score * 0.6 + compatibility * 0.4, 2)
                })
        
        opportunities.sort(key=lambda x: x['opportunity_score'], reverse=True)
        return opportunities[:10]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    init_db()
    print("🚀 Starting TikTok Trend Intelligence API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
