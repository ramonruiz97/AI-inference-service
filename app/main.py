from fastapi import FastAPI
import asyncio
import time

app = FastAPI(title = "AI Interference API", version = "0.0.1")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/ping-async")
async def async_ping():
    await asyncio.sleep(10) #This do not stop event-loop
    # time.sleep(10) #This stops event loop, so different petitions cannot be adressed
    return {"ping": "pong"}