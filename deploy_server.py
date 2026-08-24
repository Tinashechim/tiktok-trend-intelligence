import os
import json
import hashlib
import secrets
import random
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///trend_intelligence.db")
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))

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
    source = Column(String(50), default="fallback")
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
    follower_count = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.05)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)

# Seed sample trends if empty
db_seed = SessionLocal()
if db_seed.query(Trend).count() == 0:
    seed_trends = [
        {"trend_type": "format", "trend_name": "AI Filter Trend", "video_count": 120000, "growth_rate": 340, "trend_score": 100, "competition_level": "Medium", "trend_stage": "🚀 Early", "source": "fallback"},
        {"trend_type": "topic", "trend_name": "Transformation Challenge", "video_count": 89000, "growth_rate": 280, "trend_score": 100, "competition_level": "Low", "trend_stage": "🔥 Emerging", "source": "fallback"},
        {"trend_type": "format", "trend_name": "Silent Review", "video_count": 280000, "growth_rate": 220, "trend_score": 65, "competition_level": "Medium", "trend_stage": "🔥 Emerging", "source": "fallback"},
        {"trend_type": "hashtag", "trend_name": "#MoneyTok", "video_count": 340000, "growth_rate": 210, "trend_score": 60, "competition_level": "High", "trend_stage": "🔥 Emerging", "source": "fallback"},
        {"trend_type": "hashtag", "trend_name": "#CozyGaming", "video_count": 450000, "growth_rate": 180, "trend_score": 49, "competition_level": "High", "trend_stage": "📈 Rising", "source": "fallback"},
        {"trend_type": "hashtag", "trend_name": "#StudyTok", "video_count": 410000, "growth_rate": 150, "trend_score": 45, "competition_level": "High", "trend_stage": "📈 Rising", "source": "fallback"},
        {"trend_type": "hashtag", "trend_name": "#BookTok", "video_count": 890000, "growth_rate": 120, "trend_score": 31, "competition_level": "Very High", "trend_stage": "📈 Rising", "source": "fallback"},
        {"trend_type": "hashtag", "trend_name": "#FitTok", "video_count": 670000, "growth_rate": 95, "trend_score": 28, "competition_level": "Very High", "trend_stage": "📈 Rising", "source": "fallback"},
        {"trend_type": "hashtag", "trend_name": "#CleanTok", "video_count": 1800000, "growth_rate": 65, "trend_score": 16, "competition_level": "Very High", "trend_stage": "📈 Rising", "source": "fallback"},
        {"trend_type": "topic", "trend_name": "GRWM", "video_count": 3100000, "growth_rate": 45, "trend_score": 11, "competition_level": "Very High", "trend_stage": "Peak", "source": "fallback"},
    ]
    for st in seed_trends:
        st["expires_at"] = datetime.utcnow() + timedelta(hours=24)
        db_seed.add(Trend(**st))
    db_seed.commit()
db_seed.close()


app = FastAPI(title="TikTok Trend Intelligence API", version="9.0.0")

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


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserProfileCreate(BaseModel):
    username: str
    niche: str
    follower_count: int = 0
    engagement_rate: float = 0.05
    goals: List[str] = []
    sub_niches: List[str] = []
    interests: List[str] = []


class SaveTrendRequest(BaseModel):
    user_id: int
    trend_id: int


class UpgradeRequest(BaseModel):
    user_id: int
    promo_code: str = ""


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_token(user_id: int, username: str) -> str:
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    # simple JWT-like encoding (we use PyJWT in requirements)
    try:
        import jwt
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    except Exception:
        return f"tok_{user_id}"


def verify_token(token: str):
    try:
        import jwt
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return None


def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload


MOVEMENT_NAMES = {
    "peace_sign": "Peace Sign",
    "hands_up_jumping": "Jumping Hands Up",
    "pointing": "Pointing",
    "head_nod": "Head Nod",
    "fist_pump": "Fist Pump",
}

LOCATIONS = [
    "United States", "United Kingdom", "South Africa", "Nigeria", "Kenya",
    "India", "Canada", "Australia", "Brazil", "Germany", "France",
    "Japan", "South Korea", "Mexico", "Philippines", "Indonesia",
    "Netherlands", "Spain", "Italy", "Poland"
]


def get_trend_locations(trend):
    h = int(hashlib.md5(trend.trend_name.encode()).hexdigest(), 16)
    rng = random.Random(h)
    locs = LOCATIONS[:]
    rng.shuffle(locs)
    return locs[:3 + h % 3]


@app.get("/")
async def root():
    return {"message": "TikTok Trend Intelligence API", "status": "active", "version": "9.0.0"}


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
            "source": t.source,
        }
        for t in trends
    ]


@app.get("/api/trends/{trend_id}/analysis")
async def get_trend_analysis(trend_id: int, db=Depends(get_db)):
    trend = db.query(Trend).filter_by(id=trend_id).first()
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")

    if trend.trend_type == "sound":
        top_videos = [
            {"title": f"Using {trend.trend_name} - Creator A", "views": random.randint(500000, 5000000), "likes": random.randint(50000, 500000), "unique_factor": "Perfect timing with beat drop"},
            {"title": f"Creative use of {trend.trend_name} - Creator B", "views": random.randint(300000, 3000000), "likes": random.randint(30000, 300000), "unique_factor": "Unexpected transition"},
        ]
    elif trend.trend_type == "hashtag":
        top_videos = [
            {"title": f"Best example of {trend.trend_name}", "views": random.randint(400000, 4000000), "likes": random.randint(40000, 400000), "unique_factor": "Clear demonstration"},
            {"title": f"{trend.trend_name} hack", "views": random.randint(300000, 3000000), "likes": random.randint(30000, 300000), "unique_factor": "Useful tip"},
        ]
    else:
        top_videos = [
            {"title": f"{trend.trend_name} explained", "views": random.randint(350000, 3500000), "likes": random.randint(35000, 350000), "unique_factor": "Educational value"},
            {"title": f"Trying {trend.trend_name}", "views": random.randint(280000, 2800000), "likes": random.randint(28000, 280000), "unique_factor": "Authenticity"},
        ]

    factors = [v["unique_factor"] for v in top_videos]
    analysis = {
        "why_trending": f"This trend is popular because of {', '.join(factors)}.",
        "unique_angle": f"The key differentiators are {', '.join(factors)}.",
        "beat_strategy": "Use a stronger hook, add an unexpected element, optimize caption, and post at peak times."
    }
    return {"trend": trend.trend_name, "top_videos": top_videos, "analysis": analysis}


@app.get("/api/trends/movement")
async def get_movement_trends():
    movements = [
        {"pattern": "peace_sign", "movement_name": MOVEMENT_NAMES["peace_sign"], "trend_strength": 78, "description": "Peace sign gesture is trending"},
        {"pattern": "hands_up_jumping", "movement_name": MOVEMENT_NAMES["hands_up_jumping"], "trend_strength": 65, "description": "Jumping with hands up dance move"},
        {"pattern": "pointing", "movement_name": MOVEMENT_NAMES["pointing"], "trend_strength": 52, "description": "Pointing at text overlay"},
        {"pattern": "head_nod", "movement_name": MOVEMENT_NAMES["head_nod"], "trend_strength": 48, "description": "Nodding to beat"},
        {"pattern": "fist_pump", "movement_name": MOVEMENT_NAMES["fist_pump"], "trend_strength": 41, "description": "Fist pump celebration"},
    ]
    return {"movement_trends": movements, "total_detected": len(movements)}


@app.get("/api/trends/regions")
async def get_regions():
    return {"regions": LOCATIONS}


@app.get("/api/trends/{trend_id}/locations")
async def get_trend_locations_endpoint(trend_id: int, db=Depends(get_db)):
    trend = db.query(Trend).filter_by(id=trend_id).first()
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")
    locs = get_trend_locations(trend)
    return {"trend": trend.trend_name, "top_locations": locs, "is_international": len(locs) >= 4}


@app.get("/api/trends/by-region")
async def get_trends_by_region(region: str = "United States", db=Depends(get_db)):
    trends = db.query(Trend).filter(Trend.expires_at > datetime.utcnow()).order_by(Trend.trend_score.desc()).all()
    local_trends = []
    international_trends = []
    for t in trends:
        locs = get_trend_locations(t)
        item = {
            "id": t.id,
            "name": t.trend_name,
            "type": t.trend_type,
            "trend_score": t.trend_score,
            "growth_rate": t.growth_rate,
            "top_locations": locs,
            "is_international": len(locs) >= 4,
        }
        if region in locs:
            local_trends.append(item)
        else:
            international_trends.append(item)
    return {"region": region, "local_trends": local_trends[:10], "international_trends": international_trends[:10]}


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


@app.post("/api/auth/register")
async def register(user: UserRegister, db=Depends(get_db)):
    existing = db.query(User).filter((User.email == user.email) | (User.username == user.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(username=user.username, email=user.email, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_token(new_user.id, new_user.username)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email, "token": token}


@app.post("/api/auth/login")
async def login(user: UserLogin, db=Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email, User.password == hash_password(user.password)).first()
    if not existing:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(existing.id, existing.username)
    return {"id": existing.id, "username": existing.username, "email": existing.email, "token": token}


@app.post("/api/user/create")
async def create_user_profile(profile: UserProfileCreate, db=Depends(get_db)):
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
    for t in trends:
        compatibility = 65 if user.niche.lower() in t.trend_name.lower() else 35
        if "Early" in t.trend_stage or "Emerging" in t.trend_stage:
            compatibility += 10
        compatibility = min(compatibility, 100)
        opportunities.append({
            "id": t.id,
            "name": t.trend_name,
            "type": t.trend_type,
            "trend_score": t.trend_score,
            "growth_rate": t.growth_rate,
            "competition_level": t.competition_level,
            "trend_stage": t.trend_stage,
            "compatibility_score": compatibility,
            "opportunity_score": round(t.trend_score * 0.6 + compatibility * 0.4, 2),
        })
    opportunities.sort(key=lambda x: x["opportunity_score"], reverse=True)
    return {"user_niche": user.niche, "opportunities": opportunities[:10]}


@app.post("/api/user/save-trend")
async def save_trend(request: SaveTrendRequest, current_user=Depends(get_current_user)):
    try:
        with open("saved_trends.json", "r") as f:
            saved = json.load(f)
    except Exception:
        saved = {}
    user_id = str(request.user_id)
    saved.setdefault(user_id, [])
    if request.trend_id not in saved[user_id]:
        saved[user_id].append(request.trend_id)
    with open("saved_trends.json", "w") as f:
        json.dump(saved, f)
    return {"message": "Saved"}


@app.get("/api/user/saved-trends/{user_id}")
async def get_saved_trends(user_id: int, current_user=Depends(get_current_user)):
    try:
        with open("saved_trends.json", "r") as f:
            saved = json.load(f)
        return {"trend_ids": saved.get(str(user_id), [])}
    except Exception:
        return {"trend_ids": []}


@app.post("/api/premium/upgrade")
async def upgrade(request: UpgradeRequest, db=Depends(get_db)):
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_premium = True
    db.commit()
    return {"message": "Premium activated", "is_premium": True}


@app.get("/api/premium/status/{user_id}")
async def premium_status(user_id: int, db=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user.id, "is_premium": user.is_premium}


@app.post("/api/admin/trends")
async def create_trend(trend: TrendCreate, db=Depends(get_db)):
    new_trend = Trend(
        trend_type=trend.trend_type,
        trend_name=trend.trend_name,
        video_count=trend.video_count,
        growth_rate=trend.growth_rate,
        trend_score=min(100, int(trend.growth_rate / 5)),
        competition_level=trend.competition_level,
        trend_stage=trend.trend_stage,
        expires_at=datetime.utcnow() + timedelta(hours=24),
        source="manual",
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
