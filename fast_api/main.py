from typing import Union

import os
from configs.postgre_config import *
from configs.database_treatment import *
from configs.main_config import *

import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

import io
from PIL import Image

import cv2

import numpy as np

from starlette.responses import StreamingResponse, Response

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


@app.post("/upload_image/", response_class=FileResponse)
async def upload_image(file: UploadFile = File(...)):
    # try:
    requests_session = requests.session()
    print(file.filename)
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    image_np = np.array(image)
    result_img = image_np.copy()
    image_id = add_image_sql(image_np, file.filename)[0][0]
    print(image_id)
    # if car_detector_exist:
    #     car_boxes = [[]...]
    #     car_ids = add_car_sql(car_boxes, car_scores, car_types, image_id)
    # else:
    #     car_boxes = [[0,0, image_np.shape[1], image_np[0]]]...
    #     car_types = ["-"]
    #     car_scores = [1, 0.8, 0.7]
    car_boxes = [[100, 100, 200, 200], [200, 200, 400, 400], [253, 812, 364, 950]]
    car_scores = [0.9, 0.8, 0.7]
    car_types = ["car", "bus", "truck"]

    car_ids = add_car_sql(car_boxes, car_scores, car_types, image_id)
    print(car_ids)

    lp_boxes = [[[120, 120, 140, 140]], [[220, 220, 300, 300]], [[278, 820, 300, 893]]]
    lp_scores = [[0.6], [0.5], [0.4]]
    lp_types = [["region2"], ["region3"], ["unknown"]]
    lp_text = [["B125MP52"], ["O212OO77"], ["Y863TA34"]]
    for i in range(len(car_ids)):
        lp_ids = add_lp_sql(
            lp_boxes[i], lp_scores[i], lp_types[i], lp_text[i], car_ids[i][0]
        )
        if car_detector_exist:
            result_img = cv2.rectangle(
                result_img,
                pt1=(car_boxes[i][0], car_boxes[i][1]),
                pt2=(car_boxes[i][2], car_boxes[i][3]),
                color=(255, 0, 0),
                thickness=1,
            )
            cv2.putText(
                result_img,
                text=car_types[i],
                org=(car_boxes[i][0], car_boxes[i][1]),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(255, 0, 0),
                thickness=1,
            )
        for j in range(len(lp_boxes[i])):
            result_img = cv2.rectangle(
                result_img,
                pt1=(lp_boxes[i][j][0], lp_boxes[i][j][1]),
                pt2=(lp_boxes[i][j][2], lp_boxes[i][j][3]),
                color=(255, 255, 0),
                thickness=1,
            )
        cv2.putText(
            result_img,
            text=lp_text[i][j],
            org=(lp_boxes[i][j][0], lp_boxes[i][j][1]),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(255, 255, 0),
            thickness=1,
        )
        cv2.putText(
            result_img,
            text=lp_types[i][j],
            org=(lp_boxes[i][j][0], lp_boxes[i][j][1] + 30),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(255, 255, 0),
            thickness=1,
        )
        lp_ids = add_lp_sql(
            lp_boxes[i], lp_scores[i], lp_types[i], lp_text[i], car_ids[i][0]
        )
        print(lp_ids)

    cv2.imwrite(
        os.path.join(os.getcwd(), images_after_treatment, file.filename),
        cv2.cvtColor(result_img, cv2.COLOR_RGB2BGR),
    )
    # image_tensor = ToTensor()(image).unsqueeze(0).to("cuda")
    # car_boxes = triton(image)
    # lp_boxes = triton(car_boxes, image)
    # texts = triton(lp_boxes, image)

    returned_image = Image.fromarray(result_img)
    bytes_io = io.BytesIO()
    returned_image.save(bytes_io, format="PNG")
    return Response(bytes_io.getvalue(), media_type="image/png")

    return {"Status": "Error."}


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
