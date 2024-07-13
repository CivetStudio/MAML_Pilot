import os
import os.path
import re

import pyperclip
from PIL import Image

preview_url = pyperclip.paste().split('\n')
print(f'preview_url: {preview_url}')

max_width = []
max_height = []


def main_single(source, autosize=1):
    for directory, sub_directories, file_names in os.walk(source):
        for name in file_names:
            if name.lower().endswith('.png') or name.lower().endswith('.webp'):
                src = os.path.join(directory, name)
                dst = os.path.join(directory, name)
                img = Image.open(src)
                if autosize:
                    width, height = img.size
                    width += width % 2
                    height += height % 2
                else:
                    width = 720
                    height = int(1013 / 1080 * 720)
                print(f"w: {width}, h: {height}")
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                img.save(dst, 'PNG')


def main(source):
    try:
        if source.lower().endswith('.png'):
            image = Image.open(source)
            if image.mode == 'P':
                print(f"{image.mode} to RGBA")
                image = image.convert('RGBA')
            bbox = image.getbbox()
            trimmed_image = image.crop(bbox)
            trimmed_image.save(source)
            width, height = trimmed_image.size
            max_width.append(width)
            max_height.append(height)
        else:
            jpeg_image = Image.open(source)
            png_image_path = os.path.splitext(source)[0] + '.png'
            jpeg_image.save(png_image_path, 'PNG')
            jpeg_image.close()
    except Exception as e:
        print(e)


def crop_image(source, target_width, target_height, alignment="center", alignmentV="center"):
    image = Image.open(source)

    alignments = {
        "left": 0,
        "center": (image.width - target_width) // 2,
        "right": image.width - target_width
    }

    alignmentsV = {
        "top": 0,
        "center": (image.height - target_height) // 2,
        "bottom": image.height - target_height
    }

    left = alignments.get(alignment, (image.width - target_width) // 2)
    top = alignmentsV.get(alignmentV, (image.height - target_height) // 2)

    right = left + target_width
    bottom = top + target_height

    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save(source)
    print(cropped_image)
    image.close()


def fixNum(num):
    return num + (num % 2)


single_mode = len(preview_url) == 1
crop_mode = 0

if not single_mode:
    # Crop bbox
    for k in range(len(preview_url)):
        main(preview_url[k])

    if crop_mode == 0:
        w = fixNum(max(max_width) + 0)
        h = fixNum(max(max_height) + 0)

        for k in range(len(preview_url)):
            crop_image(preview_url[k], w, h, "center", "center")

        print(f"max_width: {max_width}, max_height: {max_height}")
        print(f"w: {w}, h: {h}")

else:
    for k in range(len(preview_url)):
        main_single(preview_url[k])

# 批量裁剪工具
# w = fixNum(402)
# h = fixNum(354)
#
# for k in range(len(preview_url)):
#     print(preview_url[k])
#     crop_image(preview_url[k], w, h, "center", "center")
