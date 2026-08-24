import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import random

def generate_training_data(n=500):
    data = []
    for _ in range(n):
        growth_rate = random.uniform(-10, 500)
        video_count = random.randint(1000, 3000000)
        competition = random.choice(['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        trend_type = random.choice(['sound', 'hashtag', 'topic', 'format'])
        stage = random.choice(['Early', 'Emerging', 'Rising', 'Peak', 'Declining'])
        # Label: success if growth_rate > 100 and video_count < 500000 and competition in ['Very Low','Low','Medium']
        if growth_rate > 100 and video_count < 500000 and competition in ['Very Low', 'Low', 'Medium']:
            success = 1
        else:
            success = 0
        data.append({
            'growth_rate': growth_rate,
            'video_count': video_count,
            'competition': competition,
            'type': trend_type,
            'stage': stage,
            'success': success
        })
    return pd.DataFrame(data)

# Map categorical variables
def encode_features(df):
    comp_map = {'Very Low': 1, 'Low': 2, 'Medium': 3, 'High': 4, 'Very High': 5}
    type_map = {'sound': 1, 'hashtag': 2, 'topic': 3, 'format': 4}
    stage_map = {'Early': 1, 'Emerging': 2, 'Rising': 3, 'Peak': 4, 'Declining': 5}
    df['competition_code'] = df['competition'].map(comp_map)
    df['type_code'] = df['type'].map(type_map)
    df['stage_code'] = df['stage'].map(stage_map)
    return df[['growth_rate', 'video_count', 'competition_code', 'type_code', 'stage_code']], df['success']

df = generate_training_data(500)
X, y = encode_features(df)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Model trained with accuracy: {acc:.2f}")

# Save model
joblib.dump(model, 'trend_model.pkl')
print("Saved trend_model.pkl")
