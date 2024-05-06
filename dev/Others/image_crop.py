# import pytesseract
# import easyocr
import pyperclip
from PIL import Image
import os
import os.path
import re


preview_url = pyperclip.paste().split('\n')
print(f'preview_url: {preview_url}')

max_width = []
max_height = []


def crop_image(source, left, top, target_width, target_height, alignment="center", quality=95):
    image = Image.open(source)

    right = left + target_width
    bottom = top + target_height

    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save(source, quality=quality)

    image.close()


# 判断传入文件夹或者多个文件
if len(preview_url) == 1:
    # 传入文件夹则偶数尺寸处理
    single_mode = 1
else:
    # 传入多个文件则取最大值处理
    single_mode = 0

if not single_mode:

    size = [338, 386, 774, 986]
    x, y, w, h = size[0], size[1], size[2], size[3]
    for k in range(len(preview_url)):
        crop_image(preview_url[k], x, y, w, h)

    print(f"w: {w}, h: {h}")

