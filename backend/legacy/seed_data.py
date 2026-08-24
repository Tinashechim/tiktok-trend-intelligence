from database import SessionLocal, init_db, Trend, Sound, Hashtag, UserProfile
from datetime import datetime, timedelta

def seed_data():
    db = SessionLocal()
    
    # Clear existing data
    db.query(Trend).delete()
    db.query(Sound).delete()
    db.query(Hashtag).delete()
    db.query(UserProfile).delete()
    
    # Create sample trends
    trends_data = [
        {
            "trend_type": "sound",
            "trend_name": "Epic Transition",
            "video_count": 28000,
            "growth_rate": 680,
            "engagement_rate": 15000,
            "trend_score": 95,
            "competition_level": "Very Low",
            "trend_stage": "🚀 Early",
            "expires_at": datetime.utcnow() + timedelta(hours=24)
        },
        {
            "trend_type": "sound",
            "trend_name": "Original Sound - Viral Beat",
            "video_count": 82000,
            "growth_rate": 340,
            "engagement_rate": 12000,
            "trend_score": 91,
            "competition_level": "Low",
            "trend_stage": "🔥 Emerging",
            "expires_at": datetime.utcnow() + timedelta(hours=24)
        },
        {
            "trend_type": "hashtag",
            "trend_name": "#diy",
            "video_count": 180000,
            "growth_rate": 280,
            "engagement_rate": 10000,
            "trend_score": 88,
            "competition_level": "Medium",
            "trend_stage": "📈 Rising",
            "expires_at": datetime.utcnow() + timedelta(hours=24)
        },
        {
            "trend_type": "hashtag",
            "trend_name": "#fitness",
            "video_count": 450000,
            "growth_rate": 220,
            "engagement_rate": 11000,
            "trend_score": 87,
            "competition_level": "Medium",
            "trend_stage": "📈 Rising",
            "expires_at": datetime.utcnow() + timedelta(hours=24)
        },
        {
            "trend_type": "topic",
            "trend_name": "30-day transformation",
            "video_count": 19000,
            "growth_rate": 420,
            "engagement_rate": 18000,
            "trend_score": 89,
            "competition_level": "Low",
            "trend_stage": "🔥 Emerging",
            "expires_at": datetime.utcnow() + timedelta(hours=24)
        },
        {
            "trend_type": "sound",
            "trend_name": "Lofi Chill Vibes",
            "video_count": 150000,
            "growth_rate": 45,
            "engagement_rate": 8000,
            "trend_score": 65,
            "competition_level": "High",
            "trend_stage": "Peak",
            "expires_at": datetime.utcnow() + timedelta(hours=24)
        },
        {
            "trend_type": "hashtag",
            "trend_name": "#lifehack",
            "video_count": 240000,
            "growth_rate": 175,
            "engagement_rate": 9000,
            "trend_score": 80,
            "competition_level": "Medium",
            "trend_stage": "📈 Rising",
            "expires_at": datetime.utcnow() + timedelta(hours=24)
        },
        {
            "trend_type": "topic",
            "trend_name": "Day in the life",
            "video_count": 320000,
            "growth_rate": 95,
            "engagement_rate": 7500,
            "trend_score": 70,
            "competition_level": "High",
            "trend_stage": "Peak",
            "expires_at": datetime.utcnow() + timedelta(hours=24)
        },
    ]
    
    for trend_data in trends_data:
        trend = Trend(**trend_data)
        db.add(trend)
    
    # Create sample user profile
    user_profile = UserProfile(
        username="creator_demo",
        niche="fitness",
        sub_niches=["workout", "nutrition", "wellness"],
        interests=["fitness", "health", "lifestyle"],
        goals=["increase followers", "boost engagement", "go viral"],
        content_style={"format": "tutorial", "tone": "motivational"},
        follower_count=5000,
        engagement_rate=0.06
    )
    db.add(user_profile)
    
    db.commit()
    print("✅ Sample data seeded successfully!")
    print(f"   - {len(trends_data)} trends created")
    print("   - 1 user profile created")
    
    db.close()

if __name__ == "__main__":
    init_db()
    seed_data()
