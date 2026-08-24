from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///trend_intelligence.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Trend(Base):
    __tablename__ = 'trends'
    id = Column(Integer, primary_key=True)
    trend_type = Column(String(20))
    trend_name = Column(String(500))
    video_count = Column(Integer, default=0)
    growth_rate = Column(Float, default=0.0)
    engagement_rate = Column(Float, default=0.0)
    trend_score = Column(Float, default=0.0)
    competition_level = Column(String(20))
    trend_stage = Column(String(20))
    data = Column(JSON, default=dict)
    detected_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

class UserProfile(Base):
    __tablename__ = 'user_profiles'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    niche = Column(String(100))
    sub_niches = Column(JSON, default=list)
    interests = Column(JSON, default=list)
    goals = Column(JSON, default=list)
    content_style = Column(JSON, default=dict)
    follower_count = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.05)

Base.metadata.create_all(engine)

# Seed data if empty
db = SessionLocal()
if db.query(Trend).count() == 0:
    trends_data = [
        {"trend_type": "sound", "trend_name": "Epic Transition", "video_count": 28000, "growth_rate": 680, "engagement_rate": 15000, "trend_score": 95, "competition_level": "Very Low", "trend_stage": "🚀 Early", "expires_at": datetime.utcnow() + timedelta(hours=24)},
        {"trend_type": "sound", "trend_name": "Original Sound - Viral Beat", "video_count": 82000, "growth_rate": 340, "engagement_rate": 12000, "trend_score": 91, "competition_level": "Low", "trend_stage": "🔥 Emerging", "expires_at": datetime.utcnow() + timedelta(hours=24)},
        {"trend_type": "hashtag", "trend_name": "#diy", "video_count": 180000, "growth_rate": 280, "engagement_rate": 10000, "trend_score": 88, "competition_level": "Medium", "trend_stage": "📈 Rising", "expires_at": datetime.utcnow() + timedelta(hours=24)},
        {"trend_type": "hashtag", "trend_name": "#fitness", "video_count": 450000, "growth_rate": 220, "engagement_rate": 11000, "trend_score": 87, "competition_level": "Medium", "trend_stage": "📈 Rising", "expires_at": datetime.utcnow() + timedelta(hours=24)},
        {"trend_type": "topic", "trend_name": "30-day transformation", "video_count": 19000, "growth_rate": 420, "engagement_rate": 18000, "trend_score": 89, "competition_level": "Low", "trend_stage": "🔥 Emerging", "expires_at": datetime.utcnow() + timedelta(hours=24)},
        {"trend_type": "sound", "trend_name": "Lofi Chill Vibes", "video_count": 150000, "growth_rate": 45, "engagement_rate": 8000, "trend_score": 65, "competition_level": "High", "trend_stage": "Peak", "expires_at": datetime.utcnow() + timedelta(hours=24)},
        {"trend_type": "hashtag", "trend_name": "#lifehack", "video_count": 240000, "growth_rate": 175, "engagement_rate": 9000, "trend_score": 80, "competition_level": "Medium", "trend_stage": "📈 Rising", "expires_at": datetime.utcnow() + timedelta(hours=24)},
        {"trend_type": "topic", "trend_name": "Day in the life", "video_count": 320000, "growth_rate": 95, "engagement_rate": 7500, "trend_score": 70, "competition_level": "High", "trend_stage": "Peak", "expires_at": datetime.utcnow() + timedelta(hours=24)},
    ]
    for td in trends_data:
        db.add(Trend(**td))
    db.commit()
db.close()

app = FastAPI(title="TikTok Trend Intelligence API", version="6.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TrendCreate(BaseModel):
    trend_type: str
    trend_name: str
    video_count: int = 0
    growth_rate: float = 0.0
    engagement_rate: float = 0.0
    competition_level: str = "Medium"
    trend_stage: str = "📈 Rising"

class TrendUpdate(BaseModel):
    trend_type: Optional[str] = None
    trend_name: Optional[str] = None
    video_count: Optional[int] = None
    growth_rate: Optional[float] = None
    engagement_rate: Optional[float] = None
    competition_level: Optional[str] = None
    trend_stage: Optional[str] = None

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
    return {"message": "TikTok Trend Intelligence API", "status": "active", "version": "6.0.0"}

@app.get("/api/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/api/trends/current")
async def get_trends(db=Depends(get_db)):
    trends = db.query(Trend).filter(Trend.expires_at > datetime.utcnow()).order_by(Trend.trend_score.desc()).all()
    return [{"id": t.id, "type": t.trend_type, "name": t.trend_name, "trend_score": t.trend_score, "growth_rate": t.growth_rate, "competition_level": t.competition_level, "trend_stage": t.trend_stage, "video_count": t.video_count, "engagement_rate": t.engagement_rate} for t in trends]

@app.get("/api/trends/all")
async def get_all_trends(db=Depends(get_db)):
    trends = db.query(Trend).order_by(Trend.trend_score.desc()).all()
    return [{"id": t.id, "type": t.trend_type, "name": t.trend_name, "trend_score": t.trend_score, "growth_rate": t.growth_rate, "competition_level": t.competition_level, "trend_stage": t.trend_stage, "video_count": t.video_count, "engagement_rate": t.engagement_rate} for t in trends]

@app.post("/api/admin/trends")
async def create_trend(trend: TrendCreate, db=Depends(get_db)):
    new_trend = Trend(
        trend_type=trend.trend_type,
        trend_name=trend.trend_name,
        video_count=trend.video_count,
        growth_rate=trend.growth_rate,
        engagement_rate=trend.engagement_rate,
        competition_level=trend.competition_level,
        trend_stage=trend.trend_stage,
        trend_score=min(round(trend.growth_rate / 5 + trend.engagement_rate / 1000, 2), 100),
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    db.add(new_trend)
    db.commit()
    db.refresh(new_trend)
    return {"id": new_trend.id, "message": "Trend created successfully"}

@app.put("/api/admin/trends/{trend_id}")
async def update_trend(trend_id: int, trend: TrendUpdate, db=Depends(get_db)):
    existing = db.query(Trend).filter_by(id=trend_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Trend not found")
    
    for key, value in trend.dict(exclude_unset=True).items():
        setattr(existing, key, value)
    
    db.commit()
    return {"message": "Trend updated successfully"}

@app.delete("/api/admin/trends/{trend_id}")
async def delete_trend(trend_id: int, db=Depends(get_db)):
    existing = db.query(Trend).filter_by(id=trend_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Trend not found")
    
    db.delete(existing)
    db.commit()
    return {"message": "Trend deleted successfully"}

@app.get("/api/analytics/overview")
async def get_analytics(db=Depends(get_db)):
    trends = db.query(Trend).filter(Trend.expires_at > datetime.utcnow()).all()
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
        stage_counts[trend.trend_stage] = stage_counts.get(trend.trend_stage, 0) + 1
        type_counts[trend.trend_type] = type_counts.get(trend.trend_type, 0) + 1
        growth_data.append({"name": trend.trend_name, "growth_rate": trend.growth_rate, "trend_score": trend.trend_score})
    growth_data.sort(key=lambda x: x['growth_rate'], reverse=True)
    return {"score_distribution": score_ranges, "stage_distribution": stage_counts, "type_distribution": type_counts, "growth_data": growth_data[:10], "total_analyzed": len(trends)}

@app.get("/api/calendar/best-times")
async def get_best_times():
    return {"best_days": ["Tuesday", "Wednesday", "Thursday", "Friday"], "best_times": {"Morning": "7-9 AM", "Lunch": "12-2 PM", "Evening": "7-10 PM"}, "tips": ["Post 1-2 hours before peak times", "Consistency matters more than perfect timing", "Test different times and track results"]}

@app.get("/api/calendar/weekly-plan")
async def get_weekly_plan(db=Depends(get_db)):
    trends = db.query(Trend).filter(Trend.expires_at > datetime.utcnow()).order_by(Trend.trend_score.desc()).limit(7).all()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plan = []
    for i, day in enumerate(days):
        if i < len(trends):
            t = trends[i]
            plan.append({"day": day, "trend_id": t.id, "trend_name": t.trend_name, "trend_type": t.trend_type, "trend_score": t.trend_score, "recommended_time": "7:00 PM", "content_suggestion": f"Create content around {t.trend_name}"})
        else:
            plan.append({"day": day, "trend_id": None, "trend_name": "Rest day", "trend_type": "none", "trend_score": 0, "recommended_time": "12:00 PM", "content_suggestion": "Engage with audience"})
    return {"weekly_plan": plan}

@app.post("/api/user/create")
async def create_user(profile: UserProfileCreate, db=Depends(get_db)):
    existing = db.query(UserProfile).filter_by(username=profile.username).first()
    if existing:
        existing.niche = profile.niche
        existing.follower_count = profile.follower_count
        existing.engagement_rate = profile.engagement_rate
        existing.goals = profile.goals
        user = existing
    else:
        user = UserProfile(username=profile.username, niche=profile.niche, follower_count=profile.follower_count, engagement_rate=profile.engagement_rate, goals=profile.goals, sub_niches=[], interests=[])
        db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "message": "Profile saved"}

@app.get("/api/user/{user_id}/opportunities")
async def get_opportunities(user_id: int, db=Depends(get_db)):
    user = db.query(UserProfile).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    trends = db.query(Trend).filter(Trend.expires_at > datetime.utcnow()).order_by(Trend.trend_score.desc()).all()
    opportunities = []
    for trend in trends:
        compatibility = 65 if user.niche.lower() in trend.trend_name.lower() else 35
        if trend.trend_type == 'sound': compatibility += 10
        if 'Early' in trend.trend_stage or 'Emerging' in trend.trend_stage: compatibility += 5
        compatibility = min(compatibility, 100)
        opportunity_score = round(trend.trend_score * 0.6 + compatibility * 0.4, 2)
        opportunities.append({"id": trend.id, "name": trend.trend_name, "type": trend.trend_type, "trend_score": trend.trend_score, "growth_rate": trend.growth_rate, "competition_level": trend.competition_level, "trend_stage": trend.trend_stage, "video_count": trend.video_count, "compatibility_score": round(compatibility, 2), "opportunity_score": opportunity_score})
    opportunities.sort(key=lambda x: x['opportunity_score'], reverse=True)
    return {"user_niche": user.niche, "total_opportunities": len(opportunities), "opportunities": opportunities[:10]}
