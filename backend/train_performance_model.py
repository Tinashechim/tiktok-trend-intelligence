import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import random

def generate_performance_data(n=800):
    data = []
    for _ in range(n):
        growth_rate = random.uniform(-10, 500)
        video_count = random.randint(1000, 3000000)
        competition = random.choice(['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        trend_type = random.choice(['sound', 'hashtag', 'topic', 'format'])
        follower_count = random.randint(100, 5000000)
        engagement_rate = random.uniform(0.01, 0.15)
        
        # Simulate views based on combination
        base = follower_count * random.uniform(0.05, 0.4)
        growth_factor = 1 + growth_rate / 200
        comp_factor = {'Very Low': 1.8, 'Low': 1.5, 'Medium': 1.2, 'High': 0.8, 'Very High': 0.5}[competition]
        type_factor = {'sound': 1.3, 'hashtag': 1.1, 'topic': 1.0, 'format': 1.2}[trend_type]
        views = int(base * growth_factor * comp_factor * type_factor * random.uniform(0.5, 2.0))
        likes = int(views * engagement_rate * random.uniform(0.8, 1.2))
        comments = int(likes * random.uniform(0.05, 0.15))
        shares = int(likes * random.uniform(0.02, 0.08))
        
        data.append({
            'growth_rate': growth_rate,
            'video_count': video_count,
            'competition': competition,
            'type': trend_type,
            'follower_count': follower_count,
            'engagement_rate': engagement_rate,
            'views': views,
            'likes': likes,
            'comments': comments,
            'shares': shares
        })
    return pd.DataFrame(data)

# Encode categoricals
comp_map = {'Very Low': 1, 'Low': 2, 'Medium': 3, 'High': 4, 'Very High': 5}
type_map = {'sound': 1, 'hashtag': 2, 'topic': 3, 'format': 4}

df = generate_performance_data(800)
df['competition_code'] = df['competition'].map(comp_map)
df['type_code'] = df['type'].map(type_map)

features = ['growth_rate', 'video_count', 'competition_code', 'type_code', 'follower_count', 'engagement_rate']
targets = ['views', 'likes', 'comments', 'shares']

X = df[features]
y = df[targets]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
mae_views = mean_absolute_error(y_test['views'], preds[:,0])
print(f"MAE views: {mae_views:.0f}")

joblib.dump(model, 'performance_model.pkl')
print("Saved performance_model.pkl")
