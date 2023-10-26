import cv2
import sys

sys.path.append("../configs/")


def draw_rectangle(img, bbox, t="LP", thickness=1):
    if t == "Car":
        color = (255, 0, 0)
    else:
        color = (0, 255, 0)
    img = cv2.rectangle(
        img,
        pt1=(round(bbox[0]), round(bbox[1])),
        pt2=(round(bbox[2]), round(bbox[3])),
        color=color,
        thickness=thickness,
    )
    return img


def draw_text(
    img,
    text,
    org,
    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    fontScale=0.35,
    color=(0, 255, 0),
    thickness=1,
):
    img = cv2.putText(
        img,
        text=text,
        org=(round(org[0]), round(org[1])),
        fontFace=fontFace,
        fontScale=fontScale,
        color=color,
        thickness=thickness,
    )
    return img


def draw_all_on_image(img, inp):
    (
        lp_bboxes,
        lp_types,
        lp_texts,
    ) = (
        inp[0],
        inp[1],
        inp[2],
    )
    for i in range(len(lp_bboxes)):
        img = draw_rectangle(img, lp_bboxes[i], t="LP")
        img = draw_text(
            img,
            text=lp_texts[i],
            org=[lp_bboxes[i][0], lp_bboxes[i][1] - 2],
        )
        img = draw_text(
            img,
            text=lp_types[i],
            org=[lp_bboxes[i][0], lp_bboxes[i][1] + 30],
        )
    return img
