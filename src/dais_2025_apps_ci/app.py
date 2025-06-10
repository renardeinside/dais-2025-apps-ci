from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from pydantic import BaseModel
from dais_2025_apps_ci._version import __version__ as version
import datetime as dt
from loguru import logger

app = FastAPI(
    version=version,
    title="DAIS 2025 Apps CI",
    description="A FastAPI application demonstrating CI/CD for Databricks Apps.",
    contact={"name": "Ivan Trusov", "url": "https://renardeinside.github.io/"},
)

static_path = Path(__file__).parent / "static"

logger.info(f"Starting FastAPI application with index page served from: {static_path}")


class AppInfo(BaseModel):
    version: str
    server_time: dt.datetime


# add api route which returns current package version and server time
@app.get(
    "/api/info",
    description="Get application information including version and server time.",
)
async def get_info() -> AppInfo:
    logger.info("Received request for application info")

    return AppInfo(version=version, server_time=dt.datetime.now(dt.timezone.utc))


# Serve static files from the 'static' directory
app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True))
