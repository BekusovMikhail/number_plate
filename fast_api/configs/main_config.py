images_before_treatment = "fast_api/storage/images_after_treatment"
images_after_treatment = "fast_api/storage/images_after_treatment"
symbols = (
    "0123456789авекмнорстух~",
    "0123456789ABEKMHOPCTYX~",
)
translit = {a: b for a, b in zip(*symbols)}
