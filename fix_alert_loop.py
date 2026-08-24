import re

with open('deploy_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find the broken alert_loop function
pattern = r"def alert_loop\(\):.*?(?=\ndef send_email|\Z)"
new_func = '''def alert_loop():
    while True:
        time.sleep(3600)
        try:
            import json
            with open('email_alerts.json', 'r') as f:
                alerts = json.load(f)
            if not alerts:
                continue
            db = SessionLocal()
            top_trends = db.query(Trend).filter(Trend.expires_at > datetime.utcnow()).order_by(Trend.trend_score.desc()).limit(3).all()
            db.close()
            if not top_trends:
                continue
            subject = "TrendPilot Alert: Top Opportunities"
            body = "Top trends right now:\n\n"
            for t in top_trends:
                body += f"{t.trend_name} - Score: {t.trend_score}\n"
                body += f"Growth: +{t.growth_rate}% | Competition: {t.competition_level}\n\n"
            for email, settings in alerts.items():
                send_email(email, subject, body)
        except:
            pass
'''

content = re.sub(pattern, new_func, content, flags=re.DOTALL)

with open('deploy_server.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("alert_loop fixed")
