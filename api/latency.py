from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

class RegionRequest(BaseModel):
    regions: List[str]
    threshold_ms: int

@app.post("/api/latency")
async def get_latency_metrics(request: RegionRequest):
    # Return response with 'regions' as the top-level key
    return {
        "regions": {
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
    }
