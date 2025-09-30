from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import json

app = FastAPI()

# Add CORS middleware here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allows requests from any domain
    allow_methods=["POST"], 
    allow_headers=["*"],
)

# Load your telemetry data
with open("telemetry.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

@app.post("/api/latency")
async def latency_check(request: Request):
    body = await request.json()
    regions = body.get("regions", [])
    threshold = body.get("threshold_ms", 180)

    results = {}
    for region in regions:
        region_data = df[df["region"] == region]
        if region_data.empty:
            continue

        avg_latency = region_data["latency_ms"].mean()
        p95_latency = np.percentile(region_data["latency_ms"], 95)
        avg_uptime = region_data["uptime_pct"].mean()
        breaches = (region_data["latency_ms"] > threshold).sum()

        results[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": int(breaches),
        }

    return results
