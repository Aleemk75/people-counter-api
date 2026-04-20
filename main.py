from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading
import camera
import database
@asynccontextmanager
async def lifespan(app: FastAPI):
    # start the camera in a background thread when server starts
    t = threading.Thread(target=camera.start_camera, daemon=True)
    t.start()
    print("Camera thread started")
    yield
    # nothing to clean up

app = FastAPI(lifespan=lifespan)


@app.get("/count")
def get_count():
    with camera.lock:
        return {
            "people_count": camera.current_count
        }


@app.get("/events")
def get_events():
    with camera.lock:
        return {
            "total": len(camera.events),
            "events": camera.events
        }
    

@app.get("/db-events")
def get_db_events():
    return {
        "source": "postgresql",
        "events": database.get_events()
    }    