with open('deploy_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports for JWT and hashlib
if 'import jwt' not in content:
    content = content.replace('import os', 'import os\nimport jwt\nimport hashlib\nimport secrets')

# Add secret key constant
if 'SECRET_KEY' not in content:
    content = content.replace('DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///trend_intelligence.db")', 'DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///trend_intelligence.db")\nSECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))')

# Add helper functions before auth endpoints
old_register = '@app.post("/api/auth/register")'
helpers = '''
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_token(user_id: int, username: str) -> str:
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

'''
content = content.replace(old_register, helpers + old_register)

# Update register to hash password and return token
old_register_body = '''@app.post("/api/auth/register")
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
    return {"id": new_user.id, "message": "User created"}'''

new_register_body = '''@app.post("/api/auth/register")
async def register_user(user: UserRegister, db=Depends(get_db)):
    existing = db.query(User).filter((User.email == user.email) | (User.username == user.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_token(new_user.id, new_user.username)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email, "token": token}'''

content = content.replace(old_register_body, new_register_body)

# Update login to hash password and return token
old_login_body = '''@app.post("/api/auth/login")
async def login_user(user: UserLogin, db=Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email, User.password == user.password).first()
    if not existing:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": existing.id, "username": existing.username, "email": existing.email, "token": f"tok_{existing.id}"}'''

new_login_body = '''@app.post("/api/auth/login")
async def login_user(user: UserLogin, db=Depends(get_db)):
    hashed_pw = hash_password(user.password)
    existing = db.query(User).filter(User.email == user.email, User.password == hashed_pw).first()
    if not existing:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(existing.id, existing.username)
    return {"id": existing.id, "username": existing.username, "email": existing.email, "token": token}'''

content = content.replace(old_login_body, new_login_body)

# Add JWT verification dependency for protected endpoints
old_save_trend = '@app.post("/api/user/save-trend")'
jwt_dependency = '''
from fastapi import Header

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload
'''
content = content.replace(old_save_trend, jwt_dependency + '\n\n' + old_save_trend)

# Update save-trend endpoint to require auth
old_save_body = '''@app.post("/api/user/save-trend")
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
    return {"message": "Saved"}'''

new_save_body = '''@app.post("/api/user/save-trend")
async def save_trend(request: SaveTrendRequest, current_user=Depends(get_current_user)):
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
    return {"message": "Saved"}'''

content = content.replace(old_save_body, new_save_body)

# Update get-saved-trends to require auth
old_get_saved = '''@app.get("/api/user/saved-trends/{user_id}")
async def get_saved_trends(user_id: int, db=Depends(get_db)):
    import json
    try:
        with open('saved_trends.json', 'r') as f:
            saved = json.load(f)
        return {"trend_ids": saved.get(str(user_id), [])}
    except:
        return {"trend_ids": []}'''

new_get_saved = '''@app.get("/api/user/saved-trends/{user_id}")
async def get_saved_trends(user_id: int, current_user=Depends(get_current_user)):
    import json
    try:
        with open('saved_trends.json', 'r') as f:
            saved = json.load(f)
        return {"trend_ids": saved.get(str(user_id), [])}
    except:
        return {"trend_ids": []}'''

content = content.replace(old_get_saved, new_get_saved)

with open('deploy_server.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("JWT and password hashing added")
