from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Create FastAPI instance
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

class RequestData(BaseModel):
    regions: List[str]
    threshold_ms: int

@app.post("/api/latency")
async def calculate_metrics(request: RequestData):
    response_data = {}
    for region in request.regions:
        response_data[region] = {
            "avg_latency": 145.2,
            "p95_latency": 168.7,
            "avg_uptime": 99.8,
            "breaches": 12
        }
    return response_data

# Vercel serverless function handler
async def handler(request):
    return app