from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy import func
import random

from database import SessionLocal, init_db, Trend, UserProfile

app = FastAPI(
    title="TikTok Trend Intelligence API",
    description="AI-powered trend detection for TikTok creators",
    version="3.0.0"
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
    sub_niches: List[str] = []
    interests: List[str] = []

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
        "version": "3.0.0",
        "features": [
            "Trend Detection",
            "Personalized Recommendations",
            "Content Generation",
            "Analytics Dashboard"
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
        
        sound_count = db.query(Trend).filter(Trend.trend_type == 'sound').count()
        hashtag_count = db.query(Trend).filter(Trend.trend_type == 'hashtag').count()
        topic_count = db.query(Trend).filter(Trend.trend_type == 'topic').count()
        format_count = db.query(Trend).filter(Trend.trend_type == 'format').count()
        
        return {
            "total_trends": total_trends,
            "active_trends": active_trends,
            "average_growth_rate": round(avg_growth, 2),
            "trends_by_type": {
                "sounds": sound_count,
                "hashtags": hashtag_count,
                "topics": topic_count,
                "formats": format_count
            },
            "top_trend": {
                "name": top_trend.trend_name if top_trend else "N/A",
                "score": top_trend.trend_score if top_trend else 0
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/overview")
async def get_analytics(db=Depends(get_db)):
    """Get analytics data for dashboard"""
    try:
        trends = db.query(Trend).filter(
            Trend.expires_at > datetime.utcnow()
        ).all()
        
        # Score distribution
        score_ranges = {
            "90-100": 0,
            "80-89": 0,
            "70-79": 0,
            "60-69": 0,
            "Below 60": 0
        }
        
        # Stage distribution
        stage_counts = {}
        
        # Type distribution
        type_counts = {}
        
        # Growth data for charts
        growth_data = []
        
        for trend in trends:
            # Score distribution
            score = trend.trend_score
            if score >= 90:
                score_ranges["90-100"] += 1
            elif score >= 80:
                score_ranges["80-89"] += 1
            elif score >= 70:
                score_ranges["70-79"] += 1
            elif score >= 60:
                score_ranges["60-69"] += 1
            else:
                score_ranges["Below 60"] += 1
            
            # Stage distribution
            stage = trend.trend_stage
            if stage not in stage_counts:
                stage_counts[stage] = 0
            stage_counts[stage] += 1
            
            # Type distribution
            ttype = trend.trend_type
            if ttype not in type_counts:
                type_counts[ttype] = 0
            type_counts[ttype] += 1
            
            # Growth data
            growth_data.append({
                "name": trend.trend_name,
                "growth_rate": trend.growth_rate,
                "trend_score": trend.trend_score
            })
        
        # Sort growth data
        growth_data.sort(key=lambda x: x['growth_rate'], reverse=True)
        
        return {
            "score_distribution": score_ranges,
            "stage_distribution": stage_counts,
            "type_distribution": type_counts,
            "growth_data": growth_data[:10],
            "total_analyzed": len(trends)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/growth-history/{trend_id}")
async def get_growth_history(trend_id: int, db=Depends(get_db)):
    """Get simulated growth history for a trend"""
    try:
        trend = db.query(Trend).filter_by(id=trend_id).first()
        if not trend:
            raise HTTPException(status_code=404, detail="Trend not found")
        
        # Simulate 7-day growth history based on current growth rate
        history = []
        base_growth = trend.growth_rate
        
        for i in range(7, 0, -1):
            day = datetime.utcnow() - timedelta(days=i)
            # Simulate growth pattern
            if i > 4:
                growth = base_growth * 0.3
            elif i > 2:
                growth = base_growth * 0.6
            else:
                growth = base_growth
            
            history.append({
                "date": day.strftime("%Y-%m-%d"),
                "growth_rate": round(growth + random.uniform(-10, 10), 2),
                "videos": int(trend.video_count * (1 - i * 0.1))
            })
        
        return {
            "trend_name": trend.trend_name,
            "history": history
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
            existing.sub_niches = profile.sub_niches
            existing.interests = profile.interests
            user = existing
        else:
            user = UserProfile(
                username=profile.username,
                niche=profile.niche,
                follower_count=profile.follower_count,
                engagement_rate=profile.engagement_rate,
                goals=profile.goals,
                sub_niches=profile.sub_niches,
                interests=profile.interests
            )
            db.add(user)
        
        db.commit()
        db.refresh(user)
        
        return {
            "id": user.id,
            "message": "Profile saved successfully",
            "profile": {
                "username": user.username,
                "niche": user.niche,
                "follower_count": user.follower_count,
                "engagement_rate": user.engagement_rate
            }
        }
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
            compatibility = calculate_compatibility(trend, user)
            opportunity_score = round(trend.trend_score * 0.6 + compatibility * 0.4, 2)
            
            opportunities.append({
                "id": trend.id,
                "name": trend.trend_name,
                "type": trend.trend_type,
                "trend_score": trend.trend_score,
                "growth_rate": trend.growth_rate,
                "competition_level": trend.competition_level,
                "trend_stage": trend.trend_stage,
                "video_count": trend.video_count,
                "compatibility_score": round(compatibility, 2),
                "opportunity_score": opportunity_score
            })
        
        opportunities.sort(key=lambda x: x['opportunity_score'], reverse=True)
        
        return {
            "user_niche": user.niche,
            "total_opportunities": len(opportunities),
            "opportunities": opportunities[:10]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def calculate_compatibility(trend, user):
    trend_name = trend.trend_name.lower()
    user_niche = user.niche.lower() if user.niche else ""
    
    niche_keywords = {
        'fitness': ['fitness', 'workout', 'exercise', 'gym', 'muscle', 'weight', 'diet', 'yoga', 'running', 'health', 'transformation'],
        'beauty': ['beauty', 'makeup', 'skincare', 'cosmetics', 'hair', 'nails', 'glam', 'tutorial'],
        'fashion': ['fashion', 'outfit', 'style', 'clothing', 'dress', 'shoes', 'accessories', 'ootd'],
        'food': ['food', 'recipe', 'cooking', 'meal', 'baking', 'chef', 'kitchen', 'delicious', 'eat'],
        'gaming': ['game', 'gaming', 'playthrough', 'speedrun', 'minecraft', 'fortnite', 'gamer'],
        'tech': ['tech', 'programming', 'coding', 'software', 'computer', 'phone', 'ai', 'robot'],
        'music': ['music', 'song', 'cover', 'instrument', 'singer', 'beat', 'melody', 'sound'],
        'travel': ['travel', 'destination', 'vacation', 'trip', 'adventure', 'explore'],
        'education': ['education', 'learn', 'tutorial', 'study', 'tips', 'howto', 'lifehack'],
    }
    
    keywords = niche_keywords.get(user_niche, [user_niche])
    matching = sum(1 for kw in keywords if kw in trend_name)
    
    if matching == 0:
        compatibility = 30
    elif matching == 1:
        compatibility = 65
    elif matching >= 2:
        compatibility = 85
    else:
        compatibility = 50
    
    if trend.trend_type == 'sound':
        compatibility += 10
    
    if 'Early' in trend.trend_stage or 'Emerging' in trend.trend_stage:
        compatibility += 5
    
    return min(compatibility, 100)

if __name__ == "__main__":
    import uvicorn
    init_db()
    print("Starting TikTok Trend Intelligence API v3...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
