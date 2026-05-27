# FastAPI 앱 진입점 — 라우터 등록과 시드 초기화
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import init_db
from app.routers import assets, rentals


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="agentic-qa-practice — 장비 대여 API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assets.router)
app.include_router(rentals.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"app": "agentic-qa-practice", "status": "ok"}
