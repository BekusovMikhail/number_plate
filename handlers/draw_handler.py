import sys
import os
import cv2

sys.path.append("../infrastructure/")
sys.path.append("../configs/")

from database_treatment import (
    get_lp_and_cars_by_image,
)
from main_config import images_after_treatment

from drawing import (
    draw_all_on_image,
)


def draw_on_image_and_save(image_np, image_id, filename):
    result_img = draw_all_on_image(image_np, get_lp_and_cars_by_image(image_id))
    cv2.imwrite(
        os.path.join(os.getcwd(), images_after_treatment, filename),
        cv2.cvtColor(result_img, cv2.COLOR_RGB2BGR),
    )
    return result_img
