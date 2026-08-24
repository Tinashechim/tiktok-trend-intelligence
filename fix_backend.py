# Read current deploy_server.py
content = open('deploy_server.py', 'r', encoding='utf-8').read()

# Add /api/trends/all endpoint before analytics endpoint
old_analytics = '@app.get("/api/analytics/overview")'
new_endpoint = '''@app.get("/api/trends/all")
async def get_all_trends(db=Depends(get_db)):
    trends = db.query(Trend).order_by(Trend.trend_score.desc()).all()
    return [{"id": t.id, "type": t.trend_type, "name": t.trend_name, "trend_score": t.trend_score, "growth_rate": t.growth_rate, "competition_level": t.competition_level, "trend_stage": t.trend_stage, "video_count": t.video_count} for t in trends]

@app.get("/api/analytics/overview")'''
content = content.replace(old_analytics, new_endpoint)

open('deploy_server.py', 'w', encoding='utf-8').write(content)
print("Added /api/trends/all endpoint!")
