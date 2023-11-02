import logging
import os

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from starlette.responses import Response

from configs.main_config import images_after_treatment
from db import create_db, create_tables_in_db
from handlers.main_handler import get_image_after_treatment

log = logging.getLogger("uvicorn")

app = FastAPI()


@app.get("/")
async def read_root():
    """Displays greetings"""
    return {"Greetings": "Welcome to our LPR"}


@app.get("/send_image/{image_name}", response_class=FileResponse)
async def display_image(image_name: str):
    """Gets <image name>
    Returns and displays image"""
    try:
        return os.path.join(os.getcwd(), images_after_treatment, image_name)
    except Exception as ex:
        log.error(ex)


@app.post("/upload_image/", response_class=FileResponse)
async def upload_image(file: UploadFile = File(...)):
    """Posts <image file>
    Performs image processing
    Returns and displays the image after processing"""
    return Response(await get_image_after_treatment(file), media_type="image/png")


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    create_db()
    create_tables_in_db()


# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8600)
