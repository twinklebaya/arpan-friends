import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .database import create_db_and_tables
from .routers import admin, feed, persons, stats, tips
from .seed import seed_if_empty

settings = get_settings()

app = FastAPI(title="Kailash Journeys Crisis Response API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    # Vercel gives every preview deployment its own random-hash subdomain
    # (e.g. arpan-friends-mkl5dgxkp-<team>.vercel.app), so a fixed allowlist
    # entry breaks on the next deploy. Match any *.vercel.app subdomain
    # instead of chasing each new preview URL.
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


os.makedirs(os.path.join(settings.upload_dir, "tips"), exist_ok=True)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_if_empty()


app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

app.include_router(persons.router)
app.include_router(stats.router)
app.include_router(feed.router)
app.include_router(tips.router)
app.include_router(admin.router)


@app.get("/api/health")
def health():
    return {"ok": True}
