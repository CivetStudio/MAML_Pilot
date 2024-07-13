import pyperclip
from PIL import Image
import os
import os.path
import re


def crop_image(source, left, top, target_width, target_height, quality=95):
    if type(source) is not str:
        image = source

        right = left + target_width
        bottom = top + target_height

        cropped_image = image.crop((left, top, right, bottom))
        return cropped_image
    else:
        image = Image.open(source)
        right = left + target_width
        bottom = top + target_height

        cropped_image = image.crop((left, top, right, bottom))
        cropped_image.save(source, quality=quality)
        print(cropped_image)
        image.close()


if __name__ == '__main__':

    preview_url = pyperclip.paste().split('\n')
    print(f'preview_url: {preview_url}')

    max_width = []
    max_height = []

    # 判断传入文件夹或者多个文件
    if len(preview_url) == 1:
        print('请传入多个文件')
    else:
        single_mode = 0

    if not single_mode:

        size = [0, 0, 958, 1016]
        x, y, w, h = size[0], size[1], size[2], size[3]
        for k in range(len(preview_url)):
            crop_image(preview_url[k], x, y, w, h)

        print(f"w: {w}, h: {h}")

