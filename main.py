
import os
from collections import defaultdict

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

API_KEY = "ak_45rln8w59kkg9sgnszl8ogsj"
EMAIL = "22f3000616@ds.study.iitm.ac.in"

app = FastAPI(title="Event Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)

class Event(BaseModel):
    user: str
    amount: float
    ts: int

class EventBatch(BaseModel):
    events: list[Event]

@app.post("/analytics")
async def analytics(
    batch: EventBatch,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_totals = defaultdict(float)
    revenue = 0.0

    for event in batch.events:
        if event.amount > 0:
            revenue += event.amount
            user_totals[event.user] += event.amount

    top_user = (
        max(user_totals, key=user_totals.get)
        if user_totals else None
    )

    return {
        "email": EMAIL,
        "total_events": len(batch.events),
        "unique_users": len({event.user for event in batch.events}),
        "revenue": revenue,
        "top_user": top_user,
    }
