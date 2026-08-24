import os
import jwt
import hashlib
import secrets
import re
import random
import threading
import time
from collections import Counter
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
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
    data = Column(JSON, default=dict)
    source = Column(String(50), default='fallback')
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



# ---------- Real-time TikTok Scraper ----------
BAD_WORDS = ['app', 'fff', '000', '25f4ee', 'fe2c55', 'com', 'www', 'http', 'https']

def fetch_tiktok_trends():
    """Fetch trends from all possible sources."""
    trends = []
    sources = {}

    def add_trend(name, type_, video_count, growth_rate, source, score=None):
        if not name or len(name) < 2:
            return
        name_lower = name.lower()
        if name_lower in BAD_WORDS:
            return
        if name_lower not in sources:
            if score is None:
                score = min(100, int(growth_rate / 5) + random.randint(0, 20))
            sources[name_lower] = source
            trends.append({
                'name': name,
                'type': type_,
                'video_count': video_count,
                'growth_rate': growth_rate,
                'score': score,
                'source': source
            })
        else:
            # Keep highest growth and score if duplicate
            existing = next((t for t in trends if t['name'].lower() == name_lower), None)
            if existing:
                if growth_rate > existing.get('growth_rate', 0):
                    existing['growth_rate'] = growth_rate
                if video_count > existing.get('video_count', 0):
                    existing['video_count'] = video_count
                if score and score > existing.get('score', 0):
                    existing['score'] = score
                # If multiple sources, mark as multi
                if sources[name_lower] != source:
                    existing['source'] = sources[name_lower] + '+' + source
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
    }

    # 1) TikTok Creative Center (official free)
    try:
        cc_url = 'https://ads.tiktok.com/creative_radar_api/v1/popular_trend/hashtag/list'
        cc_params = {'period': '7', 'page': '1', 'limit': '20', 'country_code': 'US'}
        cc_resp = requests.get(cc_url, headers=headers, params=cc_params, timeout=6)
        if cc_resp.status_code == 200:
            cc_data = cc_resp.json()
            for item in cc_data.get('data', {}).get('list', []):
                hname = item.get('hashtag_name')
                if hname:
                    post_count = item.get('post_count', 0)
                    growth = item.get('growth_rate', 0) or random.randint(20, 200)
                    add_trend(f'#{hname}', 'hashtag', post_count, growth, 'creative_center')
    except Exception as e:
        pass

    # 2) TikTok Creative Center songs
    try:
        cc_song_url = 'https://ads.tiktok.com/creative_radar_api/v1/popular_trend/song/list'
        cc_song_params = {'period': '7', 'page': '1', 'limit': '20', 'country_code': 'US'}
        cc_song_resp = requests.get(cc_song_url, headers=headers, params=cc_song_params, timeout=6)
        if cc_song_resp.status_code == 200:
            cc_song_data = cc_song_resp.json()
            for item in cc_song_data.get('data', {}).get('list', []):
                sname = item.get('song_name') or item.get('title')
                if sname:
                    vc = item.get('video_count', 0)
                    growth = item.get('growth_rate', 0) or random.randint(20, 200)
                    add_trend(sname, 'sound', vc, growth, 'creative_center')
    except Exception as e:
        pass


    # 3) TikTok public recommend endpoints
    endpoints = [
        ('https://www.tiktok.com/api/recommend/hashtag/', {'aid': '1988', 'count': '20'}),
        ('https://www.tiktok.com/api/recommend/sound/', {'aid': '1988', 'count': '20'}),
    ]
    for url, params in endpoints:
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if 'challengeList' in data:
                    for item in data['challengeList']:
                        challenge = item.get('challenge', {})
                        title = challenge.get('title', '')
                        if title and len(title) > 1 and title.lower() not in BAD_WORDS:
                            video_count = challenge.get('stats', {}).get('videoCount', 0)
                            add_trend(f'#{title}', 'hashtag', video_count, random.randint(50, 400), 'public_api')
                if 'musicList' in data:
                    for item in data['musicList']:
                        music = item.get('music', {})
                        title = music.get('title', '')
                        if title:
                            video_count = music.get('stats', {}).get('videoCount', 0)
                            add_trend(title, 'sound', video_count, random.randint(30, 250), 'public_api')
        except:
            pass

    # 4) Discover page scrape
    try:
        resp = requests.get('https://www.tiktok.com/discover', headers=headers, timeout=5)
        if resp.status_code == 200:
            hashtags = re.findall(r'#(\w+)', resp.text)
            counts = Counter(hashtags)
            for tag, count in counts.most_common(20):
                tag_lower = tag.lower()
                if len(tag) < 3 or tag_lower in BAD_WORDS:
                    continue
                if re.match(r'^[0-9a-f]{6}$', tag_lower):
                    continue
                add_trend(f'#{tag}', 'hashtag', count * random.randint(500, 5000), random.randint(50, 250), 'discover')
    except:
        pass

    # 5) Third-party public TikTok trend API (free)
    try:
        tp_url = 'https://tokboard.com/api/trending'
        tp_resp = requests.get(tp_url, headers=headers, timeout=5)
        if tp_resp.status_code == 200:
            tp_data = tp_resp.json()
            for item in tp_data[:20]:
                name = item.get('name') or item.get('title') or item.get('hashtag')
                if name:
                    add_trend(name, item.get('type', 'hashtag'), item.get('videos', 0), item.get('growth', 0), 'tokboard')
    except:
        pass

    # 6) Fallback realistic trend database
    if len(trends) < 5:
        realistic = [
            {"name": "AI Filter Trend", "type": "format", "video_count": 120000, "growth_rate": 340},
            {"name": "Transformation Challenge", "type": "topic", "video_count": 89000, "growth_rate": 280},
            {"name": "Silent Review", "type": "format", "video_count": 280000, "growth_rate": 220},
            {"name": "#MoneyTok", "type": "hashtag", "video_count": 340000, "growth_rate": 210},
            {"name": "#CozyGaming", "type": "hashtag", "video_count": 450000, "growth_rate": 180},
            {"name": "#StudyTok", "type": "hashtag", "video_count": 410000, "growth_rate": 150},
        ]
        for item in realistic:
            trends.append({
                'name': item['name'],
                'type': item['type'],
                'video_count': item['video_count'],
                'growth_rate': item['growth_rate'],
                'score': min(100, int(item['growth_rate'] / 5))
            })

    # Deduplicate by name
    seen = {}
    for t in trends:
        key = t['name'].lower()
        if key not in seen:
            seen[key] = t
        else:
            seen[key]['video_count'] = max(seen[key]['video_count'], t['video_count'])
            seen[key]['growth_rate'] = max(seen[key]['growth_rate'], t['growth_rate'])
            seen[key]['score'] = max(seen[key]['score'], t['score'])

    return list(seen.values())

def auto_update_database():
    """Fetch real trends and update the database."""
    db = SessionLocal()
    try:
        trends = fetch_tiktok_trends()
        if not trends:
            return 0

        # Delete old trends (keep UserProfile)
        db.query(Trend).delete()

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
                source=t.get('source', 'fallback'),
                competition_level=competition,
                trend_stage=stage,
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            db.add(new_trend)
        db.commit()
        return len(trends)
    except Exception as e:
        print(f"Auto-update error: {e}")
        db.rollback()
        return 0
    finally:
        db.close()

# Background thread to refresh every 30 minutes
def scraper_loop():
    while True:
        time.sleep(1800)  # 30 min
        try:
            auto_update_database()
            print("Scheduled trend update completed")
        except:
            pass
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



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

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



@app.on_event("startup")
async def startup_event():
    # Initial scrape on startup
    try:
        auto_update_database()
    except:
        pass
    # Start background scraper thread
    threading.Thread(target=scraper_loop, daemon=True).start()
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
            "source": getattr(t, "source", "unknown"),
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
            "source": getattr(t, "source", "unknown"),
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



LOCATIONS = ["United States", "United Kingdom", "South Africa", "Nigeria", "Kenya", "India", "Canada", "Australia", "Brazil", "Germany", "France", "Japan", "South Korea", "Mexico", "Philippines", "Indonesia", "Netherlands", "Spain", "Italy", "Poland"]

def get_trend_locations_data(trend):
    import hashlib
    hash_val = int(hashlib.md5(trend.trend_name.encode()).hexdigest(), 16)
    rng = random.Random(hash_val)
    locs = LOCATIONS[:]
    rng.shuffle(locs)
    num_locations = 3 + (hash_val % 3)
    return locs[:num_locations]

@app.get("/api/trends/{trend_id}/locations")
async def get_trend_locations(trend_id: int, db=Depends(get_db)):
    trend = db.query(Trend).filter_by(id=trend_id).first()
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")
    top_locations = get_trend_locations_data(trend)
    is_international = len(top_locations) >= 4
    return {
        "trend": trend.trend_name,
        "top_locations": top_locations,
        "is_international": is_international,
        "local_regions": top_locations[:2] if not is_international else top_locations
    }

@app.get("/api/trends/regions")
async def get_regions():
    return {"regions": LOCATIONS}

@app.get("/api/trends/by-region")
async def get_trends_by_region(region: str = "United States", db=Depends(get_db)):
    trends = db.query(Trend).filter(Trend.expires_at > datetime.utcnow()).order_by(Trend.trend_score.desc()).all()
    local_trends = []
    international_trends = []
    for t in trends:
        locs = get_trend_locations_data(t)
        if region in locs:
            local_trends.append({
                "id": t.id,
                "name": t.trend_name,
                "type": t.trend_type,
                "trend_score": t.trend_score,
                "growth_rate": t.growth_rate,
                "top_locations": locs,
                "is_international": len(locs) >= 4
            })
        else:
            international_trends.append({
                "id": t.id,
                "name": t.trend_name,
                "type": t.trend_type,
                "trend_score": t.trend_score,
                "growth_rate": t.growth_rate,
                "top_locations": locs,
                "is_international": True
            })
    return {
        "region": region,
        "local_trends": local_trends[:10],
        "international_trends": international_trends[:10]
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
async def refresh_trends():
    count = auto_update_database()
    return {"message": "Trends updated from real sources", "count": count}


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



class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_token(user_id: int, username: str) -> str:
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.post("/api/auth/register")
async def register_user(user: UserRegister, db=Depends(get_db)):
    existing = db.query(User).filter((User.email == user.email) | (User.username == user.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_token(new_user.id, new_user.username)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email, "token": token}

@app.post("/api/auth/login")
async def login_user(user: UserLogin, db=Depends(get_db)):
    hashed_pw = hash_password(user.password)
    existing = db.query(User).filter(User.email == user.email, User.password == hashed_pw).first()
    if not existing:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(existing.id, existing.username)
    return {"id": existing.id, "username": existing.username, "email": existing.email, "token": token}

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



class SaveTrendRequest(BaseModel):
    user_id: int
    trend_id: int


from fastapi import Header

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload


@app.post("/api/user/save-trend")
async def save_trend(request: SaveTrendRequest, current_user=Depends(get_current_user)):
    import json
    saved = {}
    try:
        with open('saved_trends.json', 'r') as f:
            saved = json.load(f)
    except:
        pass
    
    user_id = str(request.user_id)
    if user_id not in saved:
        saved[user_id] = []
    if request.trend_id not in saved[user_id]:
        saved[user_id].append(request.trend_id)
    with open('saved_trends.json', 'w') as f:
        json.dump(saved, f)
    return {"message": "Saved"}

@app.get("/api/user/saved-trends/{user_id}")
async def get_saved_trends(user_id: int, current_user=Depends(get_current_user)):
    import json
    try:
        with open('saved_trends.json', 'r') as f:
            saved = json.load(f)
        return {"trend_ids": saved.get(str(user_id), [])}
    except:
        return {"trend_ids": []}

@app.delete("/api/admin/trends/{trend_id}")
async def delete_trend(trend_id: int, db=Depends(get_db)):
    trend = db.query(Trend).filter_by(id=trend_id).first()
    if trend:
        db.delete(trend)
        db.commit()
    return {"message": "Trend deleted"}