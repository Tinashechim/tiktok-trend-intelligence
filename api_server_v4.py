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
    version="4.0.0"
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

class SchedulePost(BaseModel):
    trend_id: int
    day: str
    time: str
    content_type: str

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
        "version": "4.0.0",
        "features": [
            "Trend Detection",
            "Personalized Recommendations",
            "Content Generation",
            "Analytics Dashboard",
            "Content Calendar"
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

@app.get("/api/analytics/overview")
async def get_analytics(db=Depends(get_db)):
    try:
        trends = db.query(Trend).filter(
            Trend.expires_at > datetime.utcnow()
        ).all()
        
        score_ranges = {"90-100": 0, "80-89": 0, "70-79": 0, "60-69": 0, "Below 60": 0}
        stage_counts = {}
        type_counts = {}
        growth_data = []
        
        for trend in trends:
            score = trend.trend_score
            if score >= 90: score_ranges["90-100"] += 1
            elif score >= 80: score_ranges["80-89"] += 1
            elif score >= 70: score_ranges["70-79"] += 1
            elif score >= 60: score_ranges["60-69"] += 1
            else: score_ranges["Below 60"] += 1
            
            stage = trend.trend_stage
            stage_counts[stage] = stage_counts.get(stage, 0) + 1
            
            ttype = trend.trend_type
            type_counts[ttype] = type_counts.get(ttype, 0) + 1
            
            growth_data.append({
                "name": trend.trend_name,
                "growth_rate": trend.growth_rate,
                "trend_score": trend.trend_score
            })
        
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

@app.get("/api/calendar/best-times")
async def get_best_posting_times():
    """Get recommended posting times based on engagement patterns"""
    return {
        "best_days": ["Tuesday", "Wednesday", "Thursday", "Friday"],
        "best_times": {
            "Morning": "7:00 AM - 9:00 AM",
            "Lunch": "12:00 PM - 2:00 PM",
            "Evening": "7:00 PM - 10:00 PM"
        },
        "tips": [
            "Post 1-2 hours before peak engagement times",
            "Consistency is more important than perfect timing",
            "Test different times and track your results",
            "Weekends often have lower competition"
        ]
    }

@app.get("/api/calendar/weekly-plan")
async def get_weekly_plan(db=Depends(get_db)):
    """Generate a weekly content plan based on trends"""
    try:
        trends = db.query(Trend).filter(
            Trend.expires_at > datetime.utcnow()
        ).order_by(Trend.trend_score.desc()).limit(7).all()
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        plan = []
        
        for i, day in enumerate(days):
            if i < len(trends):
                trend = trends[i]
                plan.append({
                    "day": day,
                    "trend_id": trend.id,
                    "trend_name": trend.trend_name,
                    "trend_type": trend.trend_type,
                    "trend_score": trend.trend_score,
                    "recommended_time": "7:00 PM",
                    "content_suggestion": f"Create content around {trend.trend_name}"
                })
            else:
                plan.append({
                    "day": day,
                    "trend_id": None,
                    "trend_name": "Rest day or repost",
                    "trend_type": "none",
                    "trend_score": 0,
                    "recommended_time": "12:00 PM",
                    "content_suggestion": "Engage with audience or plan next week"
                })
        
        return {"weekly_plan": plan}
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
    
    if matching == 0: compatibility = 30
    elif matching == 1: compatibility = 65
    elif matching >= 2: compatibility = 85
    else: compatibility = 50
    
    if trend.trend_type == 'sound': compatibility += 10
    if 'Early' in trend.trend_stage or 'Emerging' in trend.trend_stage: compatibility += 5
    
    return min(compatibility, 100)

if __name__ == "__main__":
    import uvicorn
    init_db()
    print("Starting TikTok Trend Intelligence API v4...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
