from app.middleware import add_request_id
from app.models import PredictIn, PredictOut
from app.predictor import predict_dummy
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
def predict(payload: PredictIn) -> PredictOut:
    start_time = time.perf_counter()
    results = predict_dummy(payload.texts, payload.top_k or 1)
    #Usual microservices for more traceability
    time_ms = int((time.perf_counter() - start_time) * 1_000)
    return PredictOut(results = results, processing_ms= time_ms)
