import cv2
import numpy as np
import tritonclient.http as httpclient
import mmcv
import argparse
import os


class TritonInference:
    def __init__(self, url="127.0.0.1:8400"):
        self.client = httpclient.InferenceServerClient(url=url)

    def __img_detector_preprocess(self, image, dim=(640, 640)):
        shape = image.shape[:2]
        scale_factor = 640 / max(shape)
        image = mmcv.imrescale(
            img=image,
            scale=scale_factor,
            interpolation="area" if scale_factor < 1 else "bilinear",
        )
        new_shape = image.shape[:2]
        padding_h, padding_w = [
            dim[0] - image.shape[0],
            dim[1] - image.shape[1],
        ]
        top_padding, left_padding = int(round(padding_h // 2 - 0.1)), int(
            round(padding_w // 2 - 0.1)
        )
        bottom_padding = padding_h - top_padding
        right_padding = padding_w - left_padding

        padding_list = [
            top_padding,
            bottom_padding,
            left_padding,
            right_padding,
        ]
        image = mmcv.impad(
            img=image,
            padding=(
                padding_list[2],
                padding_list[0],
                padding_list[3],
                padding_list[1],
            ),
            pad_val=(114, 114, 114),
            padding_mode="constant",
        )
        img_preprocessed = image.transpose(2, 0, 1)
        img_preprocessed = img_preprocessed.astype("float32") / 255.0
        img_preprocessed = np.expand_dims(img_preprocessed, axis=0)
        return img_preprocessed, {
            "shape": shape,
            "new_shape": new_shape,
            "padding_list": padding_list,
        }

    def __get_detection_res(self, img_preprocessed):
        detection_input = httpclient.InferInput(
            "images", img_preprocessed.shape, datatype="FP32"
        )
        detection_input.set_data_from_numpy(img_preprocessed, binary_data=True)
        detection_response = self.client.infer(
            model_name="lp_detection", inputs=[detection_input]
        )
        boxes = detection_response.as_numpy("boxes")[0]
        scores = detection_response.as_numpy("scores")[0]
        labels = detection_response.as_numpy("labels")[0]
        return boxes, scores, labels

    def __postprocessing(
        self, boxes, scores, labels, shapes_info, score_thr=0.4
    ):
        filtered_boxes = []
        filtered_scores = []
        filtered_labels = []
        for i in range(len(boxes)):
            if scores[i] > score_thr:
                tb = [
                    shapes_info["shape"][1]
                    * (boxes[i][0] - shapes_info["padding_list"][2])
                    / shapes_info["new_shape"][1],
                    shapes_info["shape"][0]
                    * (boxes[i][1] - shapes_info["padding_list"][0])
                    / shapes_info["new_shape"][0],
                    shapes_info["shape"][1]
                    * (boxes[i][2] - shapes_info["padding_list"][2])
                    / shapes_info["new_shape"][1],
                    shapes_info["shape"][0]
                    * (boxes[i][3] - shapes_info["padding_list"][0])
                    / shapes_info["new_shape"][0],
                ]
                tb[0] = 0 if tb[0] < 0 else tb[0]
                tb[1] = 0 if tb[1] < 0 else tb[1]
                tb[2] = 0 if tb[2] < 0 else tb[2]
                tb[3] = 0 if tb[3] < 0 else tb[3]
                # tb = [tb[0], tb[1], tb[2]-tb[0], tb[3]-tb[1]]
                filtered_boxes.append(tb)
                filtered_scores.append(scores[i])
                filtered_labels.append(labels[i])

        return filtered_boxes, filtered_scores, filtered_labels

    def inf_plate_detector(self, frame: np.array):
        img_preprocessed, shapes_info = self.__img_detector_preprocess(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        )
        boxes, scores, labels = self.__get_detection_res(img_preprocessed)
        boxes, scores, labels = self.__postprocessing(
            boxes, scores, labels, shapes_info
        )
        return {"bboxes": boxes, "scores": scores, "labels": labels}

    def inf_car_detector(self, frame: np.array):
        pass

    def inf_plate_ocr(self, frame: np.array):
        pass  # TODO
