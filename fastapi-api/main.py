from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from datetime import datetime

app = FastAPI()

NODE_API_URL = os.getenv("NODE_API_URL", "http://node-api:3001")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4201",
        "http://localhost:4202",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {
        "service": "fastapi-api",
        "status": "ok",
        "time": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/raw-data")
async def raw_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NODE_API_URL}/data", timeout=10)
        return response.json()

@app.get("/data")
async def processed_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NODE_API_URL}/data", timeout=10)
        payload = response.json()

    items = payload.get("items", [])
    total = len(items)
    healthy = len([x for x in items if x["status"] == "healthy"])
    warning = len([x for x in items if x["status"] == "warning"])
    critical = len([x for x in items if x["status"] == "critical"])

    return {
        "source": "fastapi-api",
        "fetched_from": "node-api",
        "time": datetime.utcnow().isoformat() + "Z",
        "summary": {
            "total": total,
            "healthy": healthy,
            "warning": warning,
            "critical": critical
        },
        "items": items
    }