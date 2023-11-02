import io

import numpy as np
from PIL import Image

from fast_api.db import add_car, add_image
from fast_api.infrastructure.inference_model import TritonInference

from .draw_handler import draw_on_image_and_save
from .lp_detection_handler import lp_detection_treatment
from .ocr_handler import lp_ocr_treatment

triton = TritonInference()


async def get_image_after_treatment(file):
    # create_db()
    # create_tables_in_db()
    # triton = TritonInference()
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    image_np = np.array(image)
    image_id = add_image(image_np, file.filename)
    result_img = image_np.copy()
    car_boxes = np.array([[0, 0, image_np.shape[1], image_np.shape[0]]])
    car_ids = add_car(car_boxes, image_id)

    lp_boxes, lp_scores = lp_detection_treatment(image_np, triton)
    try:
        [_[0] for _ in lp_boxes]
        lp_ocr_treatment(image_np, triton, lp_boxes, lp_scores, car_ids)
        result_img = draw_on_image_and_save(result_img, image_id, file.filename)
    except:
        pass

    returned_image = Image.fromarray(result_img)
    bytes_io = io.BytesIO()
    returned_image.save(bytes_io, format="PNG")
    return_value = bytes_io.getvalue()
    return return_value
