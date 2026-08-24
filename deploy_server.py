import os
import random
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///trend_intelligence.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Trend(Base):
    __tablename__ = "trends"
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
    __tablename__ = "user_profiles"
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
db_seed = SessionLocal()
if db_seed.query(Trend).count() == 0:
    seed_trends = [
        {"trend_type": "format", "trend_name": "AI Filter Trend", "video_count": 120000, "growth_rate": 340, "trend_score": 100, "competition_level": "Medium", "trend_stage": "🚀 Early"},
        {"trend_type": "topic", "trend_name": "Transformation Challenge", "video_count": 89000, "growth_rate": 280, "trend_score": 100, "competition_level": "Low", "trend_stage": "🔥 Emerging"},
        {"trend_type": "format", "trend_name": "Silent Review", "video_count": 280000, "growth_rate": 220, "trend_score": 65, "competition_level": "Medium", "trend_stage": "🔥 Emerging"},
        {"trend_type": "hashtag", "trend_name": "#MoneyTok", "video_count": 340000, "growth_rate": 210, "trend_score": 60, "competition_level": "High", "trend_stage": "🔥 Emerging"},
        {"trend_type": "hashtag", "trend_name": "#CozyGaming", "video_count": 450000, "growth_rate": 180, "trend_score": 49, "competition_level": "High", "trend_stage": "📈 Rising"},
        {"trend_type": "hashtag", "trend_name": "#StudyTok", "video_count": 410000, "growth_rate": 150, "trend_score": 45, "competition_level": "High", "trend_stage": "📈 Rising"},
        {"trend_type": "hashtag", "trend_name": "#BookTok", "video_count": 890000, "growth_rate": 120, "trend_score": 31, "competition_level": "Very High", "trend_stage": "📈 Rising"},
        {"trend_type": "hashtag", "trend_name": "#FitTok", "video_count": 670000, "growth_rate": 95, "trend_score": 28, "competition_level": "Very High", "trend_stage": "📈 Rising"},
        {"trend_type": "hashtag", "trend_name": "#CleanTok", "video_count": 1800000, "growth_rate": 65, "trend_score": 16, "competition_level": "Very High", "trend_stage": "📈 Rising"},
        {"trend_type": "topic", "trend_name": "GRWM", "video_count": 3100000, "growth_rate": 45, "trend_score": 11, "competition_level": "Very High", "trend_stage": "Peak"},
    ]
    for st in seed_trends:
        st["expires_at"] = datetime.utcnow() + timedelta(hours=24)
        db_seed.add(Trend(**st))
    db_seed.commit()
db_seed.close()


app = FastAPI(title="TikTok Trend Intelligence API", version="8.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TrendCreate(BaseModel):
    trend_name: str
    trend_type: str = "hashtag"
    video_count: int = 0
    growth_rate: float = 0.0
    competition_level: str = "Medium"
    trend_stage: str = "📈 Rising"


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


MOVEMENT_NAMES = {
    "peace_sign": {"name": "Peace Sign", "source": "comments"},
    "hands_up_jumping": {"name": "Jumping Hands Up", "source": "local_lingo"},
    "pointing": {"name": "Pointing", "source": "comments"},
    "head_nod": {"name": "Head Nod", "source": "comments"},
    "fist_pump": {"name": "Fist Pump", "source": "local_lingo"},
}


def generate_top_videos(trend):
    if trend.trend_type == "sound":
        return [
            {"title": f"Using {trend.trend_name} - Creator A", "views": random.randint(500000, 5000000), "likes": random.randint(50000, 500000), "comments": random.randint(1000, 10000), "unique_factor": "Perfect timing with beat drop"},
            {"title": f"Creative use of {trend.trend_name} - Creator B", "views": random.randint(300000, 3000000), "likes": random.randint(30000, 300000), "comments": random.randint(800, 8000), "unique_factor": "Unexpected transition"},
            {"title": f"{trend.trend_name} dance challenge - Creator C", "views": random.randint(200000, 2000000), "likes": random.randint(20000, 200000), "comments": random.randint(500, 5000), "unique_factor": "High energy choreography"},
        ]
    elif trend.trend_type == "hashtag":
        return [
            {"title": f"Best example of {trend.trend_name}", "views": random.randint(400000, 4000000), "likes": random.randint(40000, 400000), "comments": random.randint(800, 8000), "unique_factor": "Clear demonstration"},
            {"title": f"{trend.trend_name} hack", "views": random.randint(300000, 3000000), "likes": random.randint(30000, 300000), "comments": random.randint(600, 6000), "unique_factor": "Useful tip"},
            {"title": f"{trend.trend_name} reaction", "views": random.randint(250000, 2500000), "likes": random.randint(25000, 250000), "comments": random.randint(400, 4000), "unique_factor": "Emotional hook"},
        ]
    else:
        return [
            {"title": f"{trend.trend_name} explained", "views": random.randint(350000, 3500000), "likes": random.randint(35000, 350000), "comments": random.randint(700, 7000), "unique_factor": "Educational value"},
            {"title": f"Trying {trend.trend_name}", "views": random.randint(280000, 2800000), "likes": random.randint(28000, 280000), "comments": random.randint(500, 5000), "unique_factor": "Authenticity"},
            {"title": f"{trend.trend_name} transformation", "views": random.randint(220000, 2200000), "likes": random.randint(22000, 220000), "comments": random.randint(450, 4500), "unique_factor": "Before/after hook"},
        ]


def generate_trend_analysis(trend, top_videos):
    factors = [v["unique_factor"] for v in top_videos]
    return {
        "why_trending": f"This trend is popular because of {', '.join(factors)}. It connects with the audience emotionally and offers high relatability.",
        "unique_angle": f"The key differentiators are {', '.join(factors)}. You can outperform by adding a personal twist or improving production quality.",
        "beat_strategy": "Use a stronger hook in the first 3 seconds. Add an unexpected element. Optimize caption with relevant keywords. Post at peak times for your niche.",
    }


@app.get("/")
async def root():
    return {"message": "TikTok Trend Intelligence API", "status": "active", "version": "8.0.0"}


@app.get("/api/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow()}


@app.get("/api/trends/current")
async def get_current_trends(db=Depends(get_db)):
    trends = db.query(Trend).filter(Trend.expires_at > datetime.utcnow()).order_by(Trend.trend_score.desc()).all()
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
        }
        for t in trends
    ]


@app.get("/api/trends/all")
async def get_all_trends(db=Depends(get_db)):
    trends = db.query(Trend).order_by(Trend.trend_score.desc()).all()
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
        }
        for t in trends
    ]


@app.get("/api/trends/{trend_id}/analysis")
async def get_trend_analysis(trend_id: int, db=Depends(get_db)):
    trend = db.query(Trend).filter_by(id=trend_id).first()
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")

    top_videos = generate_top_videos(trend)
    analysis = generate_trend_analysis(trend, top_videos)

    return {
        "trend": trend.trend_name,
        "top_videos": top_videos,
        "analysis": analysis,
    }


@app.get("/api/trends/movement")
async def get_movement_trends():
    movement_trends = [
        {"pattern": "peace_sign", "type": "gesture", "trend_strength": 78, "description": "Peace sign gesture is trending", "movement_name": MOVEMENT_NAMES["peace_sign"]["name"], "naming_source": MOVEMENT_NAMES["peace_sign"]["source"]},
        {"pattern": "hands_up_jumping", "type": "movement", "trend_strength": 65, "description": "Jumping with hands up dance move", "movement_name": MOVEMENT_NAMES["hands_up_jumping"]["name"], "naming_source": MOVEMENT_NAMES["hands_up_jumping"]["source"]},
        {"pattern": "pointing", "type": "gesture", "trend_strength": 52, "description": "Pointing at text overlay", "movement_name": MOVEMENT_NAMES["pointing"]["name"], "naming_source": MOVEMENT_NAMES["pointing"]["source"]},
        {"pattern": "head_nod", "type": "movement", "trend_strength": 48, "description": "Nodding to beat", "movement_name": MOVEMENT_NAMES["head_nod"]["name"], "naming_source": MOVEMENT_NAMES["head_nod"]["source"]},
        {"pattern": "fist_pump", "type": "gesture", "trend_strength": 41, "description": "Fist pump celebration", "movement_name": MOVEMENT_NAMES["fist_pump"]["name"], "naming_source": MOVEMENT_NAMES["fist_pump"]["source"]},
    ]
    return {"movement_trends": movement_trends, "total_detected": len(movement_trends)}


@app.post("/api/refresh")
async def refresh_trends(db=Depends(get_db)):
    # Simple refresh: keep existing trends and update timestamps
    trends = db.query(Trend).all()
    for t in trends:
        t.expires_at = datetime.utcnow() + timedelta(hours=24)
    db.commit()
    return {"message": "Trends refreshed", "count": len(trends)}


@app.get("/api/analytics/overview")
async def get_analytics(db=Depends(get_db)):
    trends = db.query(Trend).filter(Trend.expires_at > datetime.utcnow()).all()
    sounds = sum(1 for t in trends if t.trend_type == "sound")
    hashtags = sum(1 for t in trends if t.trend_type == "hashtag")
    topics = sum(1 for t in trends if t.trend_type == "topic")
    formats = sum(1 for t in trends if t.trend_type == "format")
    return {
        "total_trends": len(trends),
        "by_type": {"sounds": sounds, "hashtags": hashtags, "topics": topics, "formats": formats},
        "average_growth": round(sum(t.growth_rate for t in trends) / max(len(trends), 1), 2),
    }


@app.get("/api/calendar/weekly-plan")
async def get_weekly_plan(db=Depends(get_db)):
    trends = db.query(Trend).filter(Trend.expires_at > datetime.utcnow()).order_by(Trend.trend_score.desc()).limit(7).all()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plan = []
    for i, day in enumerate(days):
        if i < len(trends):
            plan.append({"day": day, "trend_name": trends[i].trend_name, "trend_score": trends[i].trend_score})
        else:
            plan.append({"day": day, "trend_name": "Rest day", "trend_score": 0})
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
        user = UserProfile(
            username=profile.username,
            niche=profile.niche,
            follower_count=profile.follower_count,
            engagement_rate=profile.engagement_rate,
            goals=profile.goals,
            sub_niches=profile.sub_niches,
            interests=profile.interests,
        )
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
        if "Early" in trend.trend_stage or "Emerging" in trend.trend_stage:
            compatibility += 10
        compatibility = min(compatibility, 100)
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
            "opportunity_score": opportunity_score,
        })
    opportunities.sort(key=lambda x: x["opportunity_score"], reverse=True)
    return {"user_niche": user.niche, "opportunities": opportunities[:10]}


@app.post("/api/admin/trends")
async def create_trend(trend: TrendCreate, db=Depends(get_db)):
    new_trend = Trend(
        trend_type=trend.trend_type,
        trend_name=trend.trend_name,
        video_count=trend.video_count,
        growth_rate=trend.growth_rate,
        trend_score=min(round(trend.growth_rate / 5), 100),
        competition_level=trend.competition_level,
        trend_stage=trend.trend_stage,
        expires_at=datetime.utcnow() + timedelta(hours=24),
    )
    db.add(new_trend)
    db.commit()
    db.refresh(new_trend)
    return {"id": new_trend.id, "message": "Trend added"}


@app.delete("/api/admin/trends/{trend_id}")
async def delete_trend(trend_id: int, db=Depends(get_db)):
    trend = db.query(Trend).filter_by(id=trend_id).first()
    if trend:
        db.delete(trend)
        db.commit()
    return {"message": "Trend deleted"}