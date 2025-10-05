from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

# COMPLETE CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow ALL origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"]  # Expose all headers to frontend
)

class RegionRequest(BaseModel):
    regions: List[str]
    threshold_ms: int

@app.post("/api/latency")
async def get_latency_metrics(request: RegionRequest):
    response_data = {
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
    
    # Create response with explicit CORS headers
    response = JSONResponse(content=response_data)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Expose-Headers"] = "*"
    return response

@app.options("/api/latency")
async def options_latency():
    response = JSONResponse(content={"status": "ok"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Expose-Headers"] = "*"
    return response
