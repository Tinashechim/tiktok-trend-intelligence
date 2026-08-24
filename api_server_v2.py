from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy import func

from database import SessionLocal, init_db, Trend, UserProfile

app = FastAPI(
    title="TikTok Trend Intelligence API",
    description="AI-powered trend detection for TikTok creators",
    version="2.0.0"
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
        "version": "2.0.0",
        "features": [
            "Trend Detection",
            "Personalized Recommendations",
            "Content Generation"
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
        
        # Count by type
        sound_count = db.query(Trend).filter(Trend.trend_type == 'sound').count()
        hashtag_count = db.query(Trend).filter(Trend.trend_type == 'hashtag').count()
        topic_count = db.query(Trend).filter(Trend.trend_type == 'topic').count()
        
        return {
            "total_trends": total_trends,
            "active_trends": active_trends,
            "average_growth_rate": round(avg_growth, 2),
            "trends_by_type": {
                "sounds": sound_count,
                "hashtags": hashtag_count,
                "topics": topic_count
            },
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

@app.get("/api/user/{user_id}")
async def get_user(user_id: int, db=Depends(get_db)):
    try:
        user = db.query(UserProfile).filter_by(id=user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "id": user.id,
            "username": user.username,
            "niche": user.niche,
            "follower_count": user.follower_count,
            "engagement_rate": user.engagement_rate,
            "goals": user.goals,
            "sub_niches": user.sub_niches,
            "interests": user.interests
        }
    except HTTPException:
        raise
    except Exception as e:
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
            trend_name = trend.trend_name.lower()
            user_niche = user.niche.lower()
            
            # Calculate compatibility
            compatibility = calculate_compatibility(trend, user)
            
            # Calculate opportunity score
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
        
        # Sort by opportunity score
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
    """Calculate compatibility between trend and user"""
    trend_name = trend.trend_name.lower()
    user_niche = user.niche.lower() if user.niche else ""
    
    # Niche keywords
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
    
    # Check for keyword matches
    matching = sum(1 for kw in keywords if kw in trend_name)
    
    # Base compatibility
    if matching == 0:
        compatibility = 30
    elif matching == 1:
        compatibility = 65
    elif matching >= 2:
        compatibility = 85
    else:
        compatibility = 50
    
    # Boost if trend is a sound (more universal)
    if trend.trend_type == 'sound':
        compatibility += 10
    
    # Boost if trend is emerging or early (less competition)
    if 'Early' in trend.trend_stage or 'Emerging' in trend.trend_stage:
        compatibility += 5
    
    return min(compatibility, 100)

if __name__ == "__main__":
    import uvicorn
    init_db()
    print("Starting TikTok Trend Intelligence API v2...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
