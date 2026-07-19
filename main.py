from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime
import os

app = FastAPI(title="MemeForge Sniper - Phase 1", version="1.0")

# ==================== CONFIG ====================
BOT_PASSWORD = os.getenv("BOT_CONTROL_PASSWORD", "change-me-in-render")

class BotConfig(BaseModel):
    mode: Literal["paper", "live"] = "paper"
    min_explosion_score: int = 65
    min_liquidity_usd: float = 50000
    max_rug_risk: int = 30
    min_token_age_minutes: int = 5
    enabled: bool = True

bot_config = BotConfig()
bot_running = False
last_scan_time = None

# ==================== MODELS ====================
class TokenInfo(BaseModel):
    address: str
    name: str
    symbol: str
    liquidity_usd: float
    volume_5m: float
    age_minutes: int
    rug_risk: int
    explosion_score: int

# ==================== HELPERS ====================
def verify_bot_password(x_bot_password: str = Header(None)):
    if x_bot_password != BOT_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid bot password")

def calculate_explosion_score(token: TokenInfo) -> int:
    """Basic scoring - we will improve this later"""
    score = 50
    if token.liquidity_usd > 100000:
        score += 15
    if token.volume_5m > 50000:
        score += 15
    if token.rug_risk < 20:
        score += 10
    if token.age_minutes > 10:
        score += 10
    return min(score, 100)

# ==================== ENDPOINTS ====================
@app.get("/")
async def root():
    return {"message": "MemeForge Sniper Phase 1 is running"}

@app.get("/health")
async def health():
    return {"status": "ok", "mode": bot_config.mode, "bot_running": bot_running}

@app.get("/scan")
async def scan_tokens():
    global last_scan_time
    last_scan_time = datetime.utcnow()
    
    # Placeholder - real scanner will be added in later phases
    example_token = TokenInfo(
        address="EXAMPLE...",
        name="Example Meme",
        symbol="EXM",
        liquidity_usd=125000,
        volume_5m=85000,
        age_minutes=12,
        rug_risk=15,
        explosion_score=78
    )
    example_token.explosion_score = calculate_explosion_score(example_token)
    
    return {
        "status": "success",
        "scanned_at": last_scan_time,
        "tokens": [example_token],
        "message": "Basic scanner active. Real Pump.fun + DexScreener coming soon."
    }

@app.get("/bot/status")
async def bot_status():
    return {
        "running": bot_running,
        "config": bot_config,
        "last_scan": last_scan_time
    }

@app.post("/bot/start", dependencies=[Depends(verify_bot_password)])
async def start_bot():
    global bot_running
    bot_running = True
    return {"status": "success", "message": f"Bot started in {bot_config.mode} mode"}

@app.post("/bot/stop", dependencies=[Depends(verify_bot_password)])
async def stop_bot():
    global bot_running
    bot_running = False
    return {"status": "success", "message": "Bot stopped"}

@app.get("/bot/config")
async def get_config():
    return bot_config

@app.post("/bot/config", dependencies=[Depends(verify_bot_password)])
async def update_config(new_config: BotConfig):
    global bot_config
    bot_config = new_config
    return {"status": "success", "config": bot_config}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
