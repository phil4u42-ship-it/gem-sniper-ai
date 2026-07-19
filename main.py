from fastapi import FastAPI, Header, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Literal
from datetime import datetime
import os

app = FastAPI(title="MemeForge Sniper - Phase 1")

BOT_PASSWORD = os.getenv("BOT_CONTROL_PASSWORD", "change-me")

class BotConfig(BaseModel):
    mode: Literal["paper", "live"] = "paper"
    min_explosion_score: int = 65
    min_liquidity_usd: float = 50000

bot_config = BotConfig()
bot_running = False

def verify_bot_password(x_bot_password: str = Header(None)):
    if x_bot_password != BOT_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    html = f"""
    <html>
    <head><title>MemeForge Sniper</title></head>
    <body style="font-family: Arial; background: #111; color: #0f0; padding: 20px;">
        <h1>🚀 MemeForge Sniper - Phase 1</h1>
        <p><strong>Status:</strong> Backend is running</p>
        <p><strong>Mode:</strong> {bot_config.mode}</p>
        <p><strong>Bot Running:</strong> {bot_running}</p>
        
        <h2>Quick Links</h2>
        <ul>
            <li><a href="/health" style="color:#0f0">Health Check</a></li>
            <li><a href="/scan" style="color:#0f0">Scanner</a></li>
            <li><a href="/bot/status" style="color:#0f0">Bot Status</a></li>
        </ul>
        
        <p style="color:#aaa">To start/stop the bot, use Hoppscotch or curl with password header.</p>
    </body>
    </html>
    """
    return html

@app.get("/health")
async def health():
    return {"status": "ok", "mode": bot_config.mode, "bot_running": bot_running}

@app.get("/scan")
async def scan():
    return {"status": "success", "message": "Scanner working (Phase 1)"}

@app.get("/bot/status")
async def status():
    return {"running": bot_running, "config": bot_config}

@app.post("/bot/start", dependencies=[Depends(verify_bot_password)])
async def start_bot():
    global bot_running
    bot_running = True
    return {"status": "success", "message": "Bot started"}

@app.post("/bot/stop", dependencies=[Depends(verify_bot_password)])
async def stop_bot():
    global bot_running
    bot_running = False
    return {"status": "success", "message": "Bot stopped"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
