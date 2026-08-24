with open('deploy_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add is_premium column to User model
if 'is_premium = Column(Boolean' not in content:
    old_user_model = "created_at = Column(DateTime, default=datetime.utcnow)"
    new_user_model = "created_at = Column(DateTime, default=datetime.utcnow)\n    is_premium = Column(Boolean, default=False)"
    content = content.replace(old_user_model, new_user_model, 1)

# Add premium endpoints before admin endpoints
old_admin = '@app.post("/api/admin/trends")'
premium_endpoints = '''
class UpgradeRequest(BaseModel):
    user_id: int
    promo_code: str = ""

@app.post("/api/premium/upgrade")
async def upgrade_to_premium(request: UpgradeRequest, db=Depends(get_db)):
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Simple promo code for testing
    if request.promo_code.upper() == "TRENDPILOT2026":
        user.is_premium = True
        db.commit()
        return {"message": "Premium activated", "is_premium": True}
    else:
        # For demo, allow any code or no code to upgrade (free)
        user.is_premium = True
        db.commit()
        return {"message": "Premium activated (demo)", "is_premium": True}

@app.get("/api/premium/status/{user_id}")
async def premium_status(user_id: int, db=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user.id, "is_premium": user.is_premium}
'''
content = content.replace(old_admin, premium_endpoints + '\n' + old_admin)

with open('deploy_server.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Premium backend added")
