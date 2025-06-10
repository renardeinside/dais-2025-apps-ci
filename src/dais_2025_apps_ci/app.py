from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from dais_2025_apps_ci._version import __version__ as version
from datetime import datetime

app = FastAPI()

# Serve static files from the 'static' directory
app.mount("/", StaticFiles(directory=Path(__file__).parent / "static"), name="static")


# add api route which returns current package version and server time
@app.get("/api/info")
async def get_info():

    current_time = datetime.now().isoformat()

    return {"version": version, "server_time": current_time}
