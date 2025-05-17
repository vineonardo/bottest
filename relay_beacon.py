import asyncio
import httpx
import os

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:8000/webhook")

async def start_summary_dispatch():
    while True:
        await asyncio.sleep(60)
        summary = {
            "status": "summary dispatch",
            "messages": 25
        }
        async with httpx.AsyncClient() as client:
            try:
                await client.post(WEBHOOK_URL, json=summary)
            except Exception as e:
                print(f"Error posting summary: {e}")
