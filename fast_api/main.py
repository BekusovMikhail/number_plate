import sys

import os

# from inference_model import TritonInference
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from starlette.responses import Response

sys.path.append("../infrastructure/")
sys.path.append("../configs/")
sys.path.append("../handlers/")

from database_treatment import (
    drop_db,
    create_db,
)
from main_handler import get_image_after_treatment
from main_config import (
    images_after_treatment,
)

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Greetings": "Welcome to our LPR"}


@app.get("/send_image/{image_name}", response_class=FileResponse)
async def display_image(image_name: str):
    return os.path.join(os.getcwd(), images_after_treatment, image_name)


@app.post("/upload_image/", response_class=FileResponse)
async def upload_image(file: UploadFile = File(...)):
    print()
    return Response(
        await get_image_after_treatment(file), media_type="image/png"
    )


@app.get("/create_db")
async def create_database():
    try:
        create_db()
        return {"Status": "Created"}
    except:
        return {
            "Status": "Not created or exist, maybe you didn't create user , go to /get_user_credentials/"
        }


@app.get("/drop_db")
async def drop_database():
    try:
        drop_db()
        return {"Status": "Dropped"}
    except:
        return {"Status": "Not dropped"}


@app.get("/get_user_credentials")
async def get_credentials_database():
    try:
        return get_db_user_credentials()
    except:
        pass
