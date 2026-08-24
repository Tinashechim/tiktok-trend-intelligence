with open('deploy_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add stripe import
if 'import stripe' not in content:
    content = content.replace('import os', 'import os\nimport stripe')

# Add Stripe config after SECRET_KEY
if 'STRIPE_SECRET_KEY' not in content:
    content = content.replace('SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))', 'SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))\nSTRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")\nSTRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")\nstripe.api_key = STRIPE_SECRET_KEY')

# Add Stripe endpoints before premium endpoints
old_premium = '@app.post("/api/premium/upgrade")'
stripe_endpoints = '''
class StripeCheckoutRequest(BaseModel):
    user_id: int

@app.post("/api/premium/create-checkout")
async def create_checkout(request: StripeCheckoutRequest, db=Depends(get_db)):
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "TrendPilot Premium"},
                    "unit_amount": 999,  # .99
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://tinashechim.github.io/tiktok-trend-intelligence/?premium=success",
            cancel_url="https://tinashechim.github.io/tiktok-trend-intelligence/?premium=cancel",
            metadata={"user_id": str(user.id)}
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/premium/webhook")
async def stripe_webhook(request: Request, db=Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Webhook error")
    
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("metadata", {}).get("user_id")
        if user_id:
            user = db.query(User).filter(User.id == int(user_id)).first()
            if user:
                user.is_premium = True
                db.commit()
    return {"message": "Webhook received"}

'''
content = content.replace(old_premium, stripe_endpoints + '\n' + old_premium)

# Import Request if not present
if 'from fastapi import Request' not in content:
    content = content.replace('from fastapi import FastAPI, HTTPException, Depends', 'from fastapi import FastAPI, HTTPException, Depends, Request')

with open('deploy_server.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Stripe backend added")
