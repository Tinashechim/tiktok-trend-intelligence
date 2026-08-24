from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
import os
import requests
import re
from collections import Counter
import random

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


@app.get("/api/trends/{trend_id}/analysis")
async def get_trend_analysis(trend_id: int, db=Depends(get_db)):
    trend = db.query(Trend).filter_by(id=trend_id).first()
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")
    
    # Simulate top videos (in production, fetch from TikTok)
    top_videos = generate_top_videos(trend)
    
    analysis = generate_trend_analysis(trend, top_videos)
    
    return {
        "trend": trend.trend_name,
        "top_videos": top_videos,
        "analysis": analysis
    }

def generate_top_videos(trend):
    videos = []
    if trend.trend_type == "sound":
        videos = [
            {"title": f"Using {trend.trend_name} - Creator A", "views": random.randint(500000, 5000000), "likes": random.randint(50000, 500000), "comments": random.randint(1000, 10000), "unique_factor": "Perfect timing with beat drop"},
            {"title": f"Creative use of {trend.trend_name} - Creator B", "views": random.randint(300000, 3000000), "likes": random.randint(30000, 300000), "comments": random.randint(800, 8000), "unique_factor": "Unexpected transition"},
            {"title": f"{trend.trend_name} dance challenge - Creator C", "views": random.randint(200000, 2000000), "likes": random.randint(20000, 200000), "comments": random.randint(500, 5000), "unique_factor": "High energy choreography"},
        ]
    elif trend.trend_type == "hashtag":
        videos = [
            {"title": f"Best example of {trend.trend_name}", "views": random.randint(400000, 4000000), "likes": random.randint(40000, 400000), "comments": random.randint(800, 8000), "unique_factor": "Clear demonstration"},
            {"title": f"{trend.trend_name} hack", "views": random.randint(300000, 3000000), "likes": random.randint(30000, 300000), "comments": random.randint(600, 6000), "unique_factor": "Useful tip"},
            {"title": f"{trend.trend_name} reaction", "views": random.randint(250000, 2500000), "likes": random.randint(25000, 250000), "comments": random.randint(400, 4000), "unique_factor": "Emotional hook"},
        ]
    else:
        videos = [
            {"title": f"{trend.trend_name} explained", "views": random.randint(350000, 3500000), "likes": random.randint(35000, 350000), "comments": random.randint(700, 7000), "unique_factor": "Educational value"},
            {"title": f"Trying {trend.trend_name}", "views": random.randint(280000, 2800000), "likes": random.randint(28000, 280000), "comments": random.randint(500, 5000), "unique_factor": "Authenticity"},
            {"title": f"{trend.trend_name} transformation", "views": random.randint(220000, 2200000), "likes": random.randint(22000, 220000), "comments": random.randint(450, 4500), "unique_factor": "Before/after hook"},
        ]
    return videos

def generate_trend_analysis(trend, top_videos):
    factors = []
    for v in top_videos:
        factors.append(v["unique_factor"])
    return {
        "why_trending": f"This trend is popular because of {', '.join(factors)}. It connects with the audience emotionally and offers high relatability.",
        "unique_angle": f"The key differentiators are {', '.join(factors)}. You can outperform by adding a personal twist or improving production quality.",
        "beat_strategy": f"To beat these videos: 1) Use a more engaging hook in first 3 seconds. 2) Add an unexpected element. 3) Optimize caption with relevant keywords. 4) Post at peak times for your niche."
    }

app = FastAPI(title="TikTok Trend Intelligence API", version="7.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class TrendCreate(BaseModel):
    trend_name: str
    trend_type: str = "hashtag"
    video_count: int = 0
    growth_rate: float = 0
    competition_level: str = "Medium"
    trend_stage: str = "📈 Rising"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fetch_real_trends():
    """Auto-fetch trends from multiple sources"""
    trends = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # Source 1: Discover Page
    try:
        resp = requests.get('https://www.tiktok.com/discover', headers=headers, timeout=5)
        if resp.status_code == 200:
            hashtags = re.findall(r'#(\w+)', resp.text)
            counts = Counter(hashtags)
            bad = ['app', 'fff', '000', '25f4ee', 'fe2c55', 'com', 'www']
            for tag, count in counts.most_common(20):
                if len(tag) < 3 or tag.lower() in bad: continue
                if re.match(r'^[0-9a-f]{6}$', tag.lower()): continue
                trends.append({
                    'name': f"#{tag}",
                    'type': 'hashtag',
                    'video_count': count * random.randint(1000, 5000),
                    'growth_rate': random.randint(50, 200),
                    'score': 70
                })
    except: pass
    
    # Source 2: Trend Database (realistic)
    database = [
        {"name": "AI Filter Trend", "type": "format", "video_count": 120000, "growth_rate": 340},
        {"name": "Transformation Challenge", "type": "topic", "video_count": 89000, "growth_rate": 280},
        {"name": "#BookTok", "type": "hashtag", "video_count": 890000, "growth_rate": 120},
        {"name": "Silent Review", "type": "format", "video_count": 280000, "growth_rate": 220},
        {"name": "#CozyGaming", "type": "hashtag", "video_count": 450000, "growth_rate": 180},
        {"name": "GRWM", "type": "topic", "video_count": 3100000, "growth_rate": 45},
        {"name": "#MoneyTok", "type": "hashtag", "video_count": 340000, "growth_rate": 210},
        {"name": "#CleanTok", "type": "hashtag", "video_count": 1800000, "growth_rate": 65},
        {"name": "#FitTok", "type": "hashtag", "video_count": 670000, "growth_rate": 95},
        {"name": "#StudyTok", "type": "hashtag", "video_count": 410000, "growth_rate": 150},
    ]
    
    for item in database:
        score = min(round(item['growth_rate'] / 5 + (300000 / max(item['video_count'], 1)) * 20), 100)
        trends.append({**item, 'score': score})
    
    return trends

def auto_update_database():
    """Auto-fetch and update database with real trends"""
    db = SessionLocal()
    
    trends = fetch_real_trends()
    
    # Clear old trends
    db.query(Trend).delete()
    
    # Add new trends
    for t in trends:
        vc = t.get('video_count', 0)
        gr = t.get('growth_rate', 0)
        
        competition = "Very Low" if vc < 50000 else "Low" if vc < 100000 else "Medium" if vc < 300000 else "High" if vc < 600000 else "Very High"
        stage = "🚀 Early" if gr > 300 else "🔥 Emerging" if gr > 200 else "📈 Rising" if gr > 50 else "Peak"
        
        new_trend = Trend(
            trend_type=t.get('type', 'hashtag'),
            trend_name=t['name'],
            video_count=vc,
            growth_rate=gr,
            engagement_rate=vc * 100,
            trend_score=t.get('score', 70),
            competition_level=competition,
            trend_stage=stage,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        db.add(new_trend)
    
    db.commit()
    db.close()
    return len(trends)

@app.get("/")
async def root():
    return {"message": "TikTok Trend Intelligence API", "status": "active", "version": "7.0.0"}


MOVEMENT_NAMES = {
    "peace_sign": {"name": "Peace Sign", "source": "comments"},
    "hands_up_jumping": {"name": "Jumping Hands Up", "source": "local_lingo"},
    "pointing": {"name": "Pointing", "source": "comments"},
    "head_nod": {"name": "Head Nod", "source": "comments"},
    "fist_pump": {"name": "Fist Pump", "source": "local_lingo"},
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

@app.get("/api/trends/movement")
async def get_movement_trends():
    """Detect and return trending movement patterns"""
    # This simulates real movement detection results
    # In production, this would analyze actual videos
    movement_trends = [
        {"pattern": "peace_sign", "type": "gesture", "trend_strength": 78, "description": "Peace sign gesture is trending"},
        {"pattern": "hands_up_jumping", "type": "movement", "trend_strength": 65, "description": "Jumping with hands up dance move"},
        {"pattern": "pointing", "type": "gesture", "trend_strength": 52, "description": "Pointing at text overlay"},
        {"pattern": "head_nod", "type": "movement", "trend_strength": 48, "description": "Nodding to beat"},
        {"pattern": "fist_pump", "type": "gesture", "trend_strength": 41, "description": "Fist pump celebration"}
    ]
    return {"movement_trends": movement_trends, "total_detected": len(movement_trends)}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/refresh")
async def refresh_trends():
    count = auto_update_database()
    return {"message": f"Trends updated", "count": count}

@app.get("/api/trends/current")
async def get_trends(db=Depends(get_db)):
    trends = db.query(Trend).filter(Trend.expires_at > datetime.utcnow()).order_by(Trend.trend_score.desc()).all()
    return [{"id": t.id, "type": t.trend_type, "name": t.trend_name, "trend_score": t.trend_score, "growth_rate": t.growth_rate, "competition_level": t.competition_level, "trend_stage": t.trend_stage, "video_count": t.video_count} for t in trends]

@app.get("/api/trends/all")
async def get_all_trends(db=Depends(get_db)):
    trends = db.query(Trend).order_by(Trend.trend_score.desc()).all()
    return [{"id": t.id, "type": t.trend_type, "name": t.trend_name, "trend_score": t.trend_score, "growth_rate": t.growth_rate, "competition_level": t.competition_level, "trend_stage": t.trend_stage, "video_count": t.video_count} for t in trends]

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
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    db.add(new_trend)
    db.commit()
    return {"message": "Trend added"}

@app.delete("/api/admin/trends/{trend_id}")
async def delete_trend(trend_id: int, db=Depends(get_db)):
    trend = db.query(Trend).filter_by(id=trend_id).first()
    if trend:
        db.delete(trend)
        db.commit()
    return {"message": "Trend deleted"}

@app.get("/api/analytics/overview")
async def get_analytics(db=Depends(get_db)):
    trends = db.query(Trend).filter(Trend.expires_at > datetime.utcnow()).all()
    total = len(trends)
    sounds = sum(1 for t in trends if t.trend_type == 'sound')
    hashtags = sum(1 for t in trends if t.trend_type == 'hashtag')
    topics = sum(1 for t in trends if t.trend_type == 'topic')
    formats = sum(1 for t in trends if t.trend_type == 'format')
    avg_growth = sum(t.growth_rate for t in trends) / max(total, 1)
    return {
        "total_trends": total,
        "by_type": {"sounds": sounds, "hashtags": hashtags, "topics": topics, "formats": formats},
        "average_growth": round(avg_growth, 2)
    }

@app.get("/api/calendar/weekly-plan")
async def get_weekly_plan(db=Depends(get_db)):
    trends = db.query(Trend).filter(Trend.expires_at > datetime.utcnow()).order_by(Trend.trend_score.desc()).limit(7).all()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plan = []
    for i, day in enumerate(days):
        if i < len(trends):
            t = trends[i]
            plan.append({"day": day, "trend_name": t.trend_name, "trend_score": t.trend_score})
        else:
            plan.append({"day": day, "trend_name": "Rest day", "trend_score": 0})
    return {"weekly_plan": plan}

@app.post("/api/user/create")
async def create_user(profile: UserProfileCreate, db=Depends(get_db)):
    existing = db.query(UserProfile).filter_by(username=profile.username).first()
    if existing:
        existing.niche = profile.niche
        user = existing
    else:
        user = UserProfile(username=profile.username, niche=profile.niche, follower_count=profile.follower_count, engagement_rate=profile.engagement_rate, goals=[], sub_niches=[], interests=[])
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
        if 'Early' in trend.trend_stage or 'Emerging' in trend.trend_stage: compatibility += 10
        compatibility = min(compatibility, 100)
        opportunity_score = round(trend.trend_score * 0.6 + compatibility * 0.4, 2)
        opportunities.append({"id": trend.id, "name": trend.trend_name, "type": trend.trend_type, "trend_score": trend.trend_score, "growth_rate": trend.growth_rate, "competition_level": trend.competition_level, "trend_stage": trend.trend_stage, "video_count": trend.video_count, "compatibility_score": round(compatibility, 2), "opportunity_score": opportunity_score})
    opportunities.sort(key=lambda x: x['opportunity_score'], reverse=True)
    return {"user_niche": user.niche, "opportunities": opportunities[:10]}

# Auto-update on startup
auto_update_database()
