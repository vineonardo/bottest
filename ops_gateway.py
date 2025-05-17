from fastapi import FastAPI, Request
import asyncio

from observer_core import launch_telegram_observer
from relay_beacon import start_summary_dispatch
from codegen_api import router as codegen_router
from log_matrix import init_db
from observer_core import launch_discord_observer


app = FastAPI()
app.include_router(codegen_router)

@app.on_event("startup")
async def on_startup():
    await init_db()
    loop = asyncio.get_event_loop()
    loop.create_task(launch_discord_observer())
    loop.create_task(launch_telegram_observer())
    loop.create_task(start_summary_dispatch())

@app.get("/ping")
async def ping():
    return {"status": "pong"}

@app.get("/status")
async def status():
    return {"service": "running"}

@app.post("/webhook")
async def receive_summary(request: Request):
    payload = await request.json()
    print("Summary webhook received:", payload)
    return {"status": "received"}

def start_api():
    import uvicorn
    uvicorn.run("ops_gateway:app", host="0.0.0.0", port=8000)

@app.on_event("shutdown")
async def shutdown():
    await app.stop()
    await app.shutdown()
