from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import auth as auth_router
from app.routers import profile as profile_router
from app.routers import calculations as calcs_router
from app.routers import reports as reports_router
from app.routers import pages as pages_router

app = FastAPI(title="Feature Assignment App", version="1.0.0")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages_router.router)
app.include_router(auth_router.router)
app.include_router(profile_router.router)
app.include_router(calcs_router.router)
app.include_router(reports_router.router)

@app.get("/health")
def health():
    return {"status": "ok"}
