with open('deploy_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Ensure UserInteraction model exists
if 'class UserInteraction' not in content:
    interaction_model = '''
class UserInteraction(Base):
    __tablename__ = "user_interactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    trend_id = Column(Integer)
    action_type = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
'''
    # Insert before Base.metadata.create_all(engine)
    content = content.replace('Base.metadata.create_all(engine)', interaction_model + '\n\nBase.metadata.create_all(engine)', 1)

# Add engagement endpoint before /api/refresh
old_refresh = '@app.post("/api/refresh")'
engagement_endpoint = '''
@app.get("/api/engagement/overview")
async def engagement_overview(db=Depends(get_db)):
    interactions = db.query(UserInteraction).all()
    trends = db.query(Trend).filter(Trend.expires_at > datetime.utcnow()).all()
    
    trend_stats = {}
    for i in interactions:
        if i.trend_id not in trend_stats:
            trend_stats[i.trend_id] = {
                'total': 0,
                'saves': 0,
                'analysis_views': 0,
                'users': set()
            }
        trend_stats[i.trend_id]['total'] += 1
        if i.action_type == 'save':
            trend_stats[i.trend_id]['saves'] += 1
        if i.action_type == 'analysis_view':
            trend_stats[i.trend_id]['analysis_views'] += 1
        trend_stats[i.trend_id]['users'].add(i.user_id)
    
    result = []
    for t in trends:
        stats = trend_stats.get(t.id, {'total': 0, 'saves': 0, 'analysis_views': 0, 'users': set()})
        unique = len(stats['users'])
        recurring = stats['total'] - unique
        engagement_score = round(
            (stats['saves'] * 3 + stats['analysis_views'] * 1 + recurring * 2) / max(1, unique),
            2
        )
        result.append({
            'trend_id': t.id,
            'trend_name': t.trend_name,
            'total_interactions': stats['total'],
            'saves': stats['saves'],
            'analysis_views': stats['analysis_views'],
            'unique_users': unique,
            'recurring_users': recurring,
            'engagement_score': engagement_score
        })
    
    result.sort(key=lambda x: x['engagement_score'], reverse=True)
    return {'total_trends': len(result), 'engagement': result[:20]}

@app.post("/api/refresh")'''
content = content.replace(old_refresh, engagement_endpoint + '\n' + old_refresh)

with open('deploy_server.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Engagement overview endpoint added")
