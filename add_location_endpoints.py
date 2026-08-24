import re

with open('deploy_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define LOCATIONS and helper functions to insert before movement endpoint
location_code = '''
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
'''

# Insert before movement endpoint
old_movement = '@app.get("/api/trends/movement")'
if old_movement in content:
    content = content.replace(old_movement, location_code + '\n' + old_movement)
    with open('deploy_server.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Location endpoints added")
else:
    print("Movement endpoint not found, cannot insert")
