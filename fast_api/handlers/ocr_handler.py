import numpy as np

from fast_api.configs.main_config import translit
from fast_api.db import add_lp


def lp_ocr_treatment(image, triton, lp_boxes, lp_scores, car_ids):
    lp_images = []
    lp_text = []
    lp_types = []
    for car in range(len(lp_boxes)):
        for bbox in lp_boxes[car]:
            lp_images.append(
                image[
                    round(bbox[1]) : round(bbox[3]),
                    round(bbox[0]) : round(bbox[2]),
                ]
            )
    labels = triton.lp_ocr.inference(np.array(lp_images))["labels"]
    for car in range(len(lp_boxes)):
        for _ in range(len(lp_boxes[car])):
            russian_text = labels[_]
            english_text = "".join([translit[x] for x in russian_text])
            lp_text.append([english_text.upper()])
            lp_types.append(["unknown"])  # type=unknown
    for i in range(len(car_ids)):
        lp_ids = add_lp(lp_boxes[i], lp_scores[i], lp_types[i], lp_text[i], car_ids[i])

    return lp_ids
