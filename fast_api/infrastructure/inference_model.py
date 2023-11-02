import tritonclient.http as httpclient

from fast_api.infrastructure.model_class import LP_OCR, LP_detector


class TritonInference:
    def __init__(self, url="inference_server:8000"):
        self.client = httpclient.InferenceServerClient(url=url)
        self.lp_detector = LP_detector(self.client)
        self.lp_ocr = LP_OCR(self.client)
