with open('deploy_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports for email
if 'import smtplib' not in content:
    content = content.replace('import os', 'import os\nimport smtplib\nfrom email.mime.text import MIMEText\nfrom email.mime.multipart import MIMEMultipart')

# Add EmailSettings model and helper after imports
if 'class EmailSettings' not in content:
    email_settings = '''
class EmailSettings(BaseModel):
    email: str
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""

def send_email(to_email, subject, body):
    try:
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER", "")
        smtp_password = os.getenv("SMTP_PASSWORD", "")
        if not smtp_user or not smtp_password:
            print("SMTP not configured")
            return False
        
        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False
'''
    # Insert before app = FastAPI()
    insert_pos = content.find('app = FastAPI(')
    if insert_pos != -1:
        content = content[:insert_pos] + email_settings + '\n' + content[insert_pos:]

# Add email subscription endpoint
old_admin = '@app.post("/api/admin/trends")'
email_endpoints = '''
@app.post("/api/alerts/subscribe")
async def subscribe_alerts(settings: EmailSettings):
    # Store subscription in file
    import json
    alerts = {}
    try:
        with open('email_alerts.json', 'r') as f:
            alerts = json.load(f)
    except:
        pass
    alerts[settings.email] = {
        "email": settings.email,
        "smtp_server": settings.smtp_server,
        "smtp_port": settings.smtp_port,
        "smtp_user": settings.smtp_user,
        "smtp_password": settings.smtp_password
    }
    with open('email_alerts.json', 'w') as f:
        json.dump(alerts, f)
    return {"message": "Subscribed to email alerts"}

@app.get("/api/alerts/status")
async def alert_status():
    import json
    try:
        with open('email_alerts.json', 'r') as f:
            alerts = json.load(f)
        return {"subscribed_count": len(alerts)}
    except:
        return {"subscribed_count": 0}
'''
content = content.replace(old_admin, email_endpoints + '\n' + old_admin)

# Add background thread to check trends and send alerts
if 'def alert_loop' not in content:
    alert_loop = '''
def alert_loop():
    while True:
        time.sleep(3600)  # check every hour
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
    # Insert before app = FastAPI()
    insert_pos = content.find('app = FastAPI(')
    if insert_pos != -1:
        content = content[:insert_pos] + alert_loop + '\n' + content[insert_pos:]

# Start alert loop in startup event
old_startup_thread = 'threading.Thread(target=scraper_loop, daemon=True).start()'
new_startup_thread = old_startup_thread + '\n    threading.Thread(target=alert_loop, daemon=True).start()'
content = content.replace(old_startup_thread, new_startup_thread)

with open('deploy_server.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Email alert backend added")
