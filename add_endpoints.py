content = open('deploy_server.py', 'r', encoding='utf-8').read()

# Add analytics and calendar endpoints before user endpoints
old_user = '@app.post("/api/user/create")'

new_endpoints = '''@app.get("/api/analytics/overview")
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

@app.post("/api/user/create")'''
content = content.replace(old_user, new_endpoints)

open('deploy_server.py', 'w', encoding='utf-8').write(content)
print("Endpoints added!")
