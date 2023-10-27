import cv2
import numpy as np
import tritonclient.http as httpclient
import mmcv
import torch
from model_class import LP_detector, LP_OCR


class TritonInference:
    def __init__(self, url="127.0.0.1:8000"):
        self.client = httpclient.InferenceServerClient(url=url)
        self.lp_detector = LP_detector(self.client)
        self.lp_ocr = LP_OCR(self.client)
