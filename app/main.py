from app.middleware import add_request_id
from app.models import PredictIn, PredictOut, Prediction
from typing import List
import time
from fastapi import FastAPI
import asyncio

app = FastAPI(title = "AI Interference API", version = "0.0.1")

app.middleware("http")(add_request_id)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/ping-async")
async def async_ping():
    await asyncio.sleep(10) #This do not stop event-loop
    # time.sleep(10) #This stops event loop, so different petitions cannot be adressed
    return {"ping": "pong"}

@app.post("/v1/predict", response_model=PredictOut)
def predict_dummy(payload: PredictIn):
    start_time = time.perf_counter()
    results: List[List[Prediction]] = [
        [Prediction(label="NEUTRAL", score=0.5)] for _ in payload.texts
    ]
    #Usual microservices for more traceability
    time_ms = int((time.perf_counter() - start_time) * 1_000)
    return PredictOut(results=results, processing_ms=time_ms)
