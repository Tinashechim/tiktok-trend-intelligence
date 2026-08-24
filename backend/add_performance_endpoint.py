with open('deploy_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'PERFORMANCE_MODEL_PATH' not in content:
    content = content.replace('MODEL_PATH = os.getenv("MODEL_PATH", "trend_model.pkl")', 'MODEL_PATH = os.getenv("MODEL_PATH", "trend_model.pkl")\nPERFORMANCE_MODEL_PATH = os.getenv("PERFORMANCE_MODEL_PATH", "performance_model.pkl")\nperformance_model = None\ntry:\n    performance_model = joblib.load(PERFORMANCE_MODEL_PATH)\n    print("Performance model loaded")\nexcept Exception as e:\n    print(f"No performance model loaded: {e}")')

# Add endpoint before health
old_health = '@app.get("/api/health")'
performance_endpoint = '''
class PerformanceRequest(BaseModel):
    trend_id: int
    user_id: int

@app.post("/api/predict-performance")
async def predict_performance(request: PerformanceRequest, db=Depends(get_db)):
    trend = db.query(Trend).filter_by(id=request.trend_id).first()
    user = db.query(User).filter_by(id=request.user_id).first() or db.query(UserProfile).filter_by(id=request.user_id).first()
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")
    if performance_model is None:
        return {"trend": trend.trend_name, "prediction": None, "message": "Model not loaded"}
    
    comp_map = {'Very Low': 1, 'Low': 2, 'Medium': 3, 'High': 4, 'Very High': 5}
    type_map = {'sound': 1, 'hashtag': 2, 'topic': 3, 'format': 4}
    stage_map = {'Early': 1, 'Emerging': 2, 'Rising': 3, 'Peak': 4, 'Declining': 5}
    
    # Use user profile if available, else defaults
    follower_count = getattr(user, 'follower_count', 10000) or 10000
    engagement_rate = getattr(user, 'engagement_rate', 0.05) or 0.05
    
    features = [
        trend.growth_rate,
        trend.video_count,
        comp_map.get(trend.competition_level, 3),
        type_map.get(trend.trend_type, 2),
        follower_count,
        engagement_rate
    ]
    
    preds = performance_model.predict([features])[0]
    return {
        "trend": trend.trend_name,
        "predicted_views": int(preds[0]),
        "predicted_likes": int(preds[1]),
        "predicted_comments": int(preds[2]),
        "predicted_shares": int(preds[3])
    }

@app.get("/api/health")'''
content = content.replace(old_health, performance_endpoint + '\n' + old_health)

with open('deploy_server.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Performance prediction endpoint added")
