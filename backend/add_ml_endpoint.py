with open('deploy_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'import joblib' not in content:
    content = content.replace('import os', 'import os\nimport joblib')

if 'MODEL_PATH' not in content:
    content = content.replace('SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))', 'SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))\nMODEL_PATH = os.getenv("MODEL_PATH", "trend_model.pkl")\nmodel = None\ntry:\n    model = joblib.load(MODEL_PATH)\n    print("ML model loaded")\nexcept Exception as e:\n    print(f"No ML model loaded: {e}")')

old_health = '@app.get("/api/health")'
prediction_code = '''
def encode_trend_for_model(trend):
    comp_map = {'Very Low': 1, 'Low': 2, 'Medium': 3, 'High': 4, 'Very High': 5}
    type_map = {'sound': 1, 'hashtag': 2, 'topic': 3, 'format': 4}
    stage_map = {'Early': 1, 'Emerging': 2, 'Rising': 3, 'Peak': 4, 'Declining': 5}
    return [
        trend.growth_rate,
        trend.video_count,
        comp_map.get(trend.competition_level, 3),
        type_map.get(trend.trend_type, 2),
        stage_map.get(trend.trend_stage.replace('🚀 ', '').replace('🔥 ', '').replace('📈 ', '').replace('📉 ', ''), 3)
    ]

@app.get("/api/predict/{trend_id}")
async def predict_trend(trend_id: int, db=Depends(get_db)):
    trend = db.query(Trend).filter_by(id=trend_id).first()
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")
    if model is None:
        return {"trend": trend.trend_name, "prediction": None, "message": "Model not loaded"}
    features = encode_trend_for_model(trend)
    proba = model.predict_proba([features])[0][1]
    return {
        "trend": trend.trend_name,
        "prediction": round(float(proba), 4),
        "success_probability": round(float(proba) * 100, 2)
    }

@app.get("/api/health")'''
content = content.replace(old_health, prediction_code + '\n' + old_health)

with open('deploy_server.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Prediction endpoint added")
