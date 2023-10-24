import sys


import os

# from inference_model import TritonInference
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

import io
from PIL import Image

import cv2

import numpy as np

from starlette.responses import Response

sys.path.append("../infrastructure/")
sys.path.append("../configs/")

from database_treatment import (
    add_image,
    add_car,
    add_lp,
    drop_db,
    create_db,
    get_lp_and_cars_by_image,
)
from drawing import draw_all_on_image
from main_config import (
    images_after_treatment,
    car_detector_exist,
    translit,
)
from inference_model import TritonInference

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Greetings": "Welcome to our LPR"}


@app.get("/send_image/{image_name}", response_class=FileResponse)
async def display_image(image_name: str):
    return os.path.join(os.getcwd(), images_after_treatment, image_name)


@app.post("/upload_image/", response_class=FileResponse)
async def upload_image(file: UploadFile = File(...)):
    # try:
    print(translit)
    triton = TritonInference()
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    image_np = np.array(image)

    result_img = image_np.copy()
    image_id = add_image(image_np, file.filename)
    if car_detector_exist:
        pass
        # car_detection_results = triton.inf_car_detector(image_np) WIP
    else:
        lp_detection_results = triton.inf_plate_detector(image_np)
        print(lp_detection_results)
        car_boxes = np.array([[0, 0, image_np.shape[1], image_np.shape[0]]])
        # car_types = ["-"]
        # car_scores = np.array([1])
        lp_boxes = np.expand_dims(lp_detection_results["bboxes"], axis=0)
        lp_scores = np.expand_dims(lp_detection_results["scores"], axis=0)
        lp_images = []
        lp_text = []
        lp_types = []
        for bbox in lp_detection_results["bboxes"]:
            lp_images.append(
                image_np[
                    round(bbox[1]) : round(bbox[3]),
                    round(bbox[0]) : round(bbox[2]),
                ]
            )
            cv2.imwrite(
                "/home/mike/python_files/plate_detection/fast_api/images_after_treatment/tmp.png",
                image_np[
                    round(bbox[1]) : round(bbox[3]),
                    round(bbox[0]) : round(bbox[2]),
                ],
            )
        labels = triton.inf_plate_recognizer(np.array(lp_images))["labels"]
        print(labels)

    for _ in range(len(lp_detection_results["bboxes"])):
        russian_text = labels[_]
        english_text = "".join([translit[x] for x in russian_text])
        lp_text.append([english_text.upper()])
        lp_types.append(["unknown"])  # type=unknown
    print(lp_text)
    car_ids = add_car(car_boxes, image_id)
    for i in range(len(car_ids)):
        lp_ids = add_lp(
            lp_boxes[i], lp_scores[i], lp_types[i], lp_text[i], car_ids[i]
        )
    result_img = draw_all_on_image(
        result_img, get_lp_and_cars_by_image(image_id)
    )
    cv2.imwrite(
        os.path.join(os.getcwd(), images_after_treatment, file.filename),
        cv2.cvtColor(result_img, cv2.COLOR_RGB2BGR),
    )

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
