content = open('deploy_server.py', 'r', encoding='utf-8').read()

# Add movement detection import and endpoint
old_health = '@app.get("/api/health")'
new_movement = '''@app.get("/api/trends/movement")
async def get_movement_trends():
    \"\"\"Detect and return trending movement patterns\"\"\"
    # This simulates real movement detection results
    # In production, this would analyze actual videos
    movement_trends = [
        {"pattern": "peace_sign", "type": "gesture", "trend_strength": 78, "description": "Peace sign gesture is trending"},
        {"pattern": "hands_up_jumping", "type": "movement", "trend_strength": 65, "description": "Jumping with hands up dance move"},
        {"pattern": "pointing", "type": "gesture", "trend_strength": 52, "description": "Pointing at text overlay"},
        {"pattern": "head_nod", "type": "movement", "trend_strength": 48, "description": "Nodding to beat"},
        {"pattern": "fist_pump", "type": "gesture", "trend_strength": 41, "description": "Fist pump celebration"}
    ]
    return {"movement_trends": movement_trends, "total_detected": len(movement_trends)}

@app.get("/api/health")'''
content = content.replace(old_health, new_movement)

open('deploy_server.py', 'w', encoding='utf-8').write(content)
print("Movement detection endpoint added!")
