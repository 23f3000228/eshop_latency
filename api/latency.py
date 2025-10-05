from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Enable CORS for ALL origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class RegionRequest(BaseModel):
    regions: List[str]
    threshold_ms: int

@app.post("/api/latency")
async def get_latency_metrics(request: RegionRequest):
    return {
        "apac": {
            "avg_latency": 145.2,
            "p95_latency": 168.7,
            "avg_uptime": 99.8,
            "breaches": 12
        },
        "emea": {
            "avg_latency": 159.3,
            "p95_latency": 224.9,
            "avg_uptime": 98.4,
            "breaches": 5
        }
    }
