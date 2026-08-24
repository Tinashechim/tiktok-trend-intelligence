content = open('deploy_server.py', 'r', encoding='utf-8').read()

# Check if analysis endpoint exists
if '/api/trends/{trend_id}/analysis' in content:
    print('Analysis endpoint already exists')
else:
    # Add endpoint before 'app = FastAPI(' or after all imports
    endpoint_code = '''
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
        "analysis": analysis
    }

def generate_top_videos(trend):
    import random
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
'''
    # Insert before app = FastAPI()
    if 'app = FastAPI(' in content:
        content = content.replace('app = FastAPI(', endpoint_code + '\napp = FastAPI(', 1)
    else:
        # If app not found, append at end
        content += endpoint_code
    
    open('deploy_server.py', 'w', encoding='utf-8').write(content)
    print('Analysis endpoint added')
