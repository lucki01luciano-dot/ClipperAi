import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import stripe

app = FastAPI(title="ClipperAI Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_placeholder")

class VideoRequest(BaseModel):
    video_url: str
    caption_preset: str = "hormozi"

class SubscriptionRequest(BaseModel):
    plan: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "ClipperAI Engine Active"}

@app.post("/api/process-video")
async def process_video(req: VideoRequest):
    if not req.video_url:
        raise HTTPException(status_code=400, detail="Video URL required")
    
    # Process video logic (yt-dlp, whisper, ffmpeg)
    return {
        "status": "success",
        "video_url": req.video_url,
        "clips": [
            {
                "id": 1,
                "title": "How AI will change software engineering forever",
                "virality_score": 98,
                "timestamp": "03:12 - 03:54"
            }
        ]
    }

@app.post("/api/create-checkout-session")
async def create_checkout_session(req: SubscriptionRequest):
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f"ClipperAI - {req.plan}"},
                    'unit_amount': 2900 if req.plan == 'Creator Pro' else 7900,
                    'recurring': {'interval': 'month'},
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url='https://yourwebsite.com/success',
            cancel_url='https://yourwebsite.com/cancel',
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        return {"checkout_url": None, "error": str(e)}
