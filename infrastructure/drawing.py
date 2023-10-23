import cv2


def draw_rectangle(img, bbox, t="LP", thickness=1):
    if t == "Car":
        color = (255, 0, 0)
    else:
        color = (0, 255, 0)
    cv2.rectangle(
        img,
        pt1=(bbox[0], bbox[1]),
        pt2=(bbox[2], bbox[3]),
        color=color,
        thickness=thickness,
    )
    return img


def draw_text(
    img, text, org, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0)
):
    cv2.putText(
        img,
        text=text,
        org=(org[0], org[1]),
        fontFace=fontFace,
        fontScale=fontScale,
        color=color,
        thickness=1,
    )
    return img
