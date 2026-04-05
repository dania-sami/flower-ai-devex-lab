from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from datetime import datetime, timedelta
import random
import statistics

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="Flower Platform Data Lab")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

RNG = random.Random(42)
NOW = datetime.now().replace(minute=0, second=0, microsecond=0)

ASSETS = [
    {"id": "BAT-SE-01", "type": "Battery", "region": "Stockholm", "capacity_mw": 80},
    {"id": "SOL-SE-07", "type": "Solar", "region": "Malmö", "capacity_mw": 46},
    {"id": "WND-SE-11", "type": "Wind", "region": "Uppsala", "capacity_mw": 122},
    {"id": "EV-SE-22", "type": "EV Cluster", "region": "Gothenburg", "capacity_mw": 35},
]


def build_series(hours: int = 48):
    points = []
    for i in range(hours):
        ts = NOW - timedelta(hours=hours - i - 1)
        base_price = 45 + 12 * (1 + __import__('math').sin(i / 6))
        demand = 220 + 25 * (1 + __import__('math').cos(i / 8)) + RNG.uniform(-10, 10)
        renewable = 155 + 30 * (1 + __import__('math').sin(i / 7)) + RNG.uniform(-12, 12)
        battery = 18 + 8 * (1 + __import__('math').cos(i / 5)) + RNG.uniform(-3, 3)
        points.append(
            {
                "timestamp": ts.isoformat(),
                "price_eur_mwh": round(base_price + RNG.uniform(-3, 3), 1),
                "demand_mw": round(demand, 1),
                "renewable_mw": round(renewable, 1),
                "battery_dispatch_mw": round(max(0, battery), 1),
                "quality_score": round(97 + RNG.uniform(-2, 2), 2),
            }
        )
    return points

SERIES = build_series()

PIPELINE_RUNS = [
    {
        "name": "raw_ingestion",
        "status": "success",
        "duration_sec": 43,
        "freshness_min": 4,
        "owner": "platform",
    },
    {
        "name": "bronze_to_silver",
        "status": "success",
        "duration_sec": 71,
        "freshness_min": 7,
        "owner": "platform",
    },
    {
        "name": "silver_to_gold_forecasts",
        "status": "success",
        "duration_sec": 95,
        "freshness_min": 11,
        "owner": "product-data",
    },
    {
        "name": "quality_checks",
        "status": "success",
        "duration_sec": 29,
        "freshness_min": 12,
        "owner": "platform",
    },
]

QUALITY_CHECKS = [
    {"name": "null_rate_threshold", "result": "pass", "detail": "0.2% nulls in market_price"},
    {"name": "duplicate_primary_keys", "result": "pass", "detail": "No duplicate asset events"},
    {"name": "dispatch_bounds", "result": "pass", "detail": "Battery dispatch within contract limits"},
    {"name": "lineage_completeness", "result": "pass", "detail": "All gold tables linked to upstream models"},
]

AGENTS = [
    {
        "name": "Ingestion Agent",
        "purpose": "Validates new source contracts and proposes ingestion configs.",
        "status": "active",
    },
    {
        "name": "Quality Agent",
        "purpose": "Runs rule checks, flags anomalies, and suggests tests.",
        "status": "active",
    },
    {
        "name": "Cost Agent",
        "purpose": "Inspects expensive jobs and recommends optimizations.",
        "status": "monitoring",
    },
]


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "flower-platform-data-lab"}


@app.get("/api/summary")
def summary():
    prices = [p["price_eur_mwh"] for p in SERIES[-24:]]
    quality = [p["quality_score"] for p in SERIES[-24:]]
    demand = [p["demand_mw"] for p in SERIES[-24:]]
    renewable = [p["renewable_mw"] for p in SERIES[-24:]]
    return {
        "platform_uptime": "99.96%",
        "avg_price": round(statistics.mean(prices), 1),
        "avg_quality": round(statistics.mean(quality), 2),
        "avg_demand": round(statistics.mean(demand), 1),
        "renewable_coverage": round(100 * statistics.mean(renewable) / statistics.mean(demand), 1),
        "successful_runs": sum(1 for r in PIPELINE_RUNS if r["status"] == "success"),
        "daily_cost_eur": 184.2,
    }


@app.get("/api/timeseries")
def timeseries():
    return JSONResponse(SERIES)


@app.get("/api/assets")
def assets():
    enriched = []
    for asset in ASSETS:
        enriched.append(
            {
                **asset,
                "availability_pct": round(96 + RNG.uniform(1, 3), 2),
                "data_latency_sec": int(20 + RNG.uniform(5, 40)),
                "events_24h": int(600 + RNG.uniform(20, 220)),
            }
        )
    return JSONResponse(enriched)


@app.get("/api/pipeline-runs")
def pipeline_runs():
    return JSONResponse(PIPELINE_RUNS)


@app.get("/api/quality")
def quality():
    return JSONResponse(QUALITY_CHECKS)


@app.get("/api/agents")
def agents():
    return JSONResponse(AGENTS)


@app.post("/api/run-demo-pipeline")
def run_demo_pipeline():
    simulated = {
        "name": "adhoc_backfill",
        "status": "success",
        "duration_sec": int(50 + RNG.uniform(10, 60)),
        "freshness_min": 1,
        "owner": "platform",
    }
    PIPELINE_RUNS.insert(0, simulated)
    return {"message": "Demo pipeline executed successfully", "run": simulated}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
