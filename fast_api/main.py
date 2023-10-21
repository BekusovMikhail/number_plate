from typing import Union

import os
from configs.postgre_config import *
from configs.database_treatment import *

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

# from typing import Annotated
import io
from PIL import Image

import cv2

import numpy as np

from torchvision.transforms import ToTensor

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Greetings": "Welcome to our LPR"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/send_image/{image_name}", response_class=FileResponse)
async def display_image(image_name: str):
    print()
    return os.path.join(os.getcwd(), images_after_treatment, image_name)


@app.post("/upload_image/")
async def upload_image(file: UploadFile = File(...)):
    # try:
    print(file.filename)
    image = Image.open(io.BytesIO(await file.read()))
    image_np = np.array(image)
    add_image_sql(image_np, file.filename)
    image_tensor = ToTensor()(image).unsqueeze(0).to("cuda")
    print(image_tensor)
    return {"Status": f"File uploaded."}
    # except:
    #     return {"Status": f"File npt uploaded."}


@app.get("/create_db")
async def create_database():
    # try:
    create_db()
    return {"Status": "Created"}


# except:
#     return {
#         "Status": "Not created or exist, maybe you didn't create user , go to /get_user_credentials/"
#     }


@app.get("/drop_db")
async def drop_database():
    # try:
    drop_db()
    return {"Status": "Dropped"}


# except:
#     return {"Status": "Not dropped"}


@app.get("/get_user_credentials")
async def get_credentials_database():
    try:
        return get_db_user_credentials()
    except:
        pass
