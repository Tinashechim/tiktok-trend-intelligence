with open('deploy_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1) Add User model (we already have UserProfile, but we'll add a separate User for auth)
if 'class User(Base):' not in content:
    user_model = '''
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
'''
    # Insert after UserProfile class
    old_userprofile_end = 'class UserProfileCreate(BaseModel):'
    content = content.replace(old_userprofile_end, user_model + '\n' + old_userprofile_end, 1)

# 2) Add auth endpoints before admin endpoints
old_admin = '@app.post("/api/admin/trends")'
auth_endpoints = '''
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/api/auth/register")
async def register_user(user: UserRegister, db=Depends(get_db)):
    # Check if user exists
    existing = db.query(User).filter((User.email == user.email) | (User.username == user.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # In production, hash the password!
    new_user = User(username=user.username, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "message": "User created"}

@app.post("/api/auth/login")
async def login_user(user: UserLogin, db=Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email, User.password == user.password).first()
    if not existing:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": existing.id, "username": existing.username, "email": existing.email, "token": f"tok_{existing.id}"}
'''
content = content.replace(old_admin, auth_endpoints + '\n' + old_admin)

# 3) Add SaveTrend model and endpoint for authenticated users
old_delete_admin = '@app.delete("/api/admin/trends/{trend_id}")'
save_endpoint = '''
class SaveTrendRequest(BaseModel):
    user_id: int
    trend_id: int

@app.post("/api/user/save-trend")
async def save_trend(request: SaveTrendRequest, db=Depends(get_db)):
    # Store saved trend in a simple table (we'll use JSON file for demo)
    import json
    saved = {}
    try:
        with open('saved_trends.json', 'r') as f:
            saved = json.load(f)
    except:
        pass
    
    user_id = str(request.user_id)
    if user_id not in saved:
        saved[user_id] = []
    if request.trend_id not in saved[user_id]:
        saved[user_id].append(request.trend_id)
    with open('saved_trends.json', 'w') as f:
        json.dump(saved, f)
    return {"message": "Saved"}

@app.get("/api/user/saved-trends/{user_id}")
async def get_saved_trends(user_id: int, db=Depends(get_db)):
    import json
    try:
        with open('saved_trends.json', 'r') as f:
            saved = json.load(f)
        return {"trend_ids": saved.get(str(user_id), [])}
    except:
        return {"trend_ids": []}
'''
content = content.replace(old_delete_admin, save_endpoint + '\n' + old_delete_admin)

with open('deploy_server.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Auth endpoints added")
