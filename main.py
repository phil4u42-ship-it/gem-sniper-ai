from fastapi import FastAPI

app = FastAPI(title="Gem Sniper AI")

@app.get("/")
async def root():
    return {"message": "Gem Sniper AI Backend is LIVE! 🚀"}

@app.get("/health")
async def health():
    return {"status": "ok"}
