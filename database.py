from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean,
    ForeignKey, Text, JSON, BigInteger, Index,
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
from datetime import datetime, timedelta

Base = declarative_base()

class Creator(Base):
    __tablename__ = 'creators'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, index=True)
    display_name = Column(String(255))
    follower_count = Column(BigInteger, default=0)
    verified = Column(Boolean, default=False)
    niche = Column(String(100), index=True)
    engagement_rate = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    videos = relationship("Video", back_populates="creator")

class Video(Base):
    __tablename__ = 'videos'
    
    id = Column(Integer, primary_key=True)
    tiktok_id = Column(String(100), unique=True, index=True)
    creator_id = Column(Integer, ForeignKey('creators.id'))
    description = Column(Text)
    hashtags = Column(JSON, default=list)
    sound_name = Column(String(255))
    video_length = Column(Float)
    format_type = Column(String(50))
    
    views_count = Column(BigInteger, default=0)
    likes_count = Column(BigInteger, default=0)
    comments_count = Column(BigInteger, default=0)
    shares_count = Column(BigInteger, default=0)
    saves_count = Column(BigInteger, default=0)
    
    engagement_velocity = Column(Float, default=0.0)
    views_velocity = Column(Float, default=0.0)
    
    posted_at = Column(DateTime(timezone=True))
    first_seen_at = Column(DateTime(timezone=True), server_default=func.now())
    last_updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    creator = relationship("Creator", back_populates="videos")

class Sound(Base):
    __tablename__ = 'sounds'
    
    id = Column(Integer, primary_key=True)
    tiktok_sound_id = Column(String(100), unique=True, index=True)
    name = Column(String(500))
    artist = Column(String(255))
    video_count = Column(Integer, default=0)
    growth_rate = Column(Float, default=0.0)
    trend_score = Column(Float, default=0.0)
    competition_level = Column(String(20))
    trend_stage = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Hashtag(Base):
    __tablename__ = 'hashtags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, index=True)
    video_count = Column(Integer, default=0)
    growth_rate = Column(Float, default=0.0)
    trend_score = Column(Float, default=0.0)
    competition_level = Column(String(20))
    trend_stage = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

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
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    
    __table_args__ = (
        Index('idx_trend_score', 'trend_score'),
    )

class UserProfile(Base):
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    niche = Column(String(100), index=True)
    sub_niches = Column(JSON, default=list)
    interests = Column(JSON, default=list)
    goals = Column(JSON, default=list)
    content_style = Column(JSON, default=dict)
    follower_count = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.05)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ContentIdea(Base):
    __tablename__ = 'content_ideas'
    
    id = Column(Integer, primary_key=True)
    user_profile_id = Column(Integer, ForeignKey('user_profiles.id'))
    trend_id = Column(Integer, ForeignKey('trends.id'))
    title = Column(String(500))
    hook = Column(Text)
    script = Column(Text)
    caption = Column(Text)
    hashtags = Column(JSON, default=list)
    suggested_sound = Column(String(255))
    video_length = Column(Integer)
    predicted_views = Column(BigInteger)
    predicted_engagement = Column(Float)
    confidence_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Create database engine
engine = create_engine('sqlite:///trend_intelligence.db', echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
    print("✅ Database initialized successfully!")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    print("Database file created: trend_intelligence.db")
