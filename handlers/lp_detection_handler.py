import numpy as np


def lp_detection_treatment(image_np, triton):
    lp_detection_results = triton.lp_detector.inference(image_np)

    lp_boxes = np.expand_dims(lp_detection_results["bboxes"], axis=0)
    lp_scores = np.expand_dims(lp_detection_results["scores"], axis=0)
    return lp_boxes, lp_scores
