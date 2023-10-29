import cv2
import numpy as np
import tritonclient.http as httpclient
import mmcv
import torch


class LP_detector:
    def __init__(self, client):
        self.client = client

    def _preprocess(self, image, dim=(640, 640)):
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

    def _get_res(self, img_preprocessed):
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

    def _postprocessing(
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

    def inference(self, frame: np.array):
        img_preprocessed, shapes_info = self._preprocess(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        )
        boxes, scores, labels = self._get_res(img_preprocessed)
        boxes, scores, labels = self._postprocessing(
            boxes, scores, labels, shapes_info
        )
        return {"bboxes": boxes, "scores": scores, "labels": labels}


class LP_OCR:
    def __init__(self, client):
        self.client = client
        self.vocabular = "0123456789авекмнорстух~"
        self.blank = "~"
        self.recognition_height = 64
        self.recognition_width = 256
        self.blank_index = self.vocabular.index(self.blank)
        self.num_to_char = dict()
        for i, c in enumerate(self.vocabular):
            self.num_to_char[i] = c

    def _image_resize(self, image):
        shape = image.shape[:2]
        r = self.recognition_height / float(shape[0])
        new_w = int(shape[1] * r)
        if new_w >= self.recognition_width:
            image = cv2.resize(
                image,
                (self.recognition_width, self.recognition_height),
                cv2.INTER_CUBIC,
            )
        else:
            delta = self.recognition_width - new_w
            image = cv2.resize(
                image, (new_w, self.recognition_height), cv2.INTER_CUBIC
            )
            pad_left = 0
            pad_right = delta

            pad_value = np.zeros(len(image.shape)) + np.median(image)
            image = cv2.copyMakeBorder(
                image,
                0,
                0,
                pad_left,
                pad_right,
                cv2.BORDER_CONSTANT,
                value=pad_value,
            )
        return image

    def _image_normalize(self, image):
        image = image.astype(np.float32) / 255
        image = (image - image.mean()) / (image.std() + 1e-8)
        return image

    def _image_preprocessing(self, images):
        batch = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = self._image_resize(img)
            img = self._image_normalize(img)
            if len(img.shape) == 2:
                img = np.concatenate(
                    [
                        np.expand_dims(img, axis=0),
                        np.expand_dims(img, axis=0),
                        np.expand_dims(img, axis=0),
                    ],
                    axis=0,
                )
                batch.append(img)
            else:
                batch.append(np.transpose(img, (2, 0, 1)))
        return np.array(batch)

    def _get_res(self, img_preprocessed):
        img_preprocessed = np.float32(img_preprocessed)
        recognition_input = httpclient.InferInput(
            "input", img_preprocessed.shape, datatype="FP32"
        )
        recognition_input.set_data_from_numpy(
            img_preprocessed, binary_data=True
        )
        recognition_response = self.client.infer(
            model_name="lp_recognition",
            inputs=[recognition_input],
        )
        return recognition_response

    def _decode_sample(self, sample):
        label = ""
        for i in sample:
            if i == self.blank_index:
                break
            label += self.num_to_char.get(i, "")
        return label

    def _postprocessing(self, batch):
        batch = torch.softmax(batch, 2)
        batch = torch.argmax(batch, 2)
        batch = batch.detach().cpu().numpy()

        labels = []
        for sample in batch:
            sample = [sample[0]] + [
                c for i, c in enumerate(sample[1:]) if c != sample[i]
            ]
            sample = [s for s in sample if s != self.blank_index]
            label = self._decode_sample(sample)
            labels.append(label)
        return labels

    def inference(self, images: np.array):
        lp_tensor = self._image_preprocessing(images)
        outputs = torch.Tensor(self._get_res(lp_tensor).as_numpy("output"))
        labels = self._postprocessing(outputs)
        return {"labels": labels}
