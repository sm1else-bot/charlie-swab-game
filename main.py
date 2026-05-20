import os
import pathlib
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv(".env")
load_dotenv(".env.local", override=True)

LAVA_API_KEY = os.getenv("LAVA_API_KEY")
LAVA_BASE_URL = os.getenv("LAVA_BASE_URL", "https://api.lava.so/v1")

app = FastAPI()


@app.post("/api/lava/chat/completions")
async def proxy_ai(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{LAVA_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {LAVA_API_KEY}",
                "Content-Type": "application/json",
            },
            json=body,
            timeout=30.0,
        )
    return JSONResponse(content=response.json(), status_code=response.status_code)


dist = pathlib.Path(__file__).parent / "dist"
if dist.exists():
    app.mount("/", StaticFiles(directory=str(dist), html=True), name="static")
