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


def main_single(source):

    walk_names = os.walk(rf'{source}')

    for (directory, sub_directorys, file_names) in walk_names:
        for name in file_names:
            m = re.match(r'(.+)\.png$', name, re.I)
            if m:
                src = os.path.join(directory, name)
                if source is not None:
                    dst = os.path.join(directory, m.group(1)) + '.png'
                    img = Image.open(src)
                    width = img.size[0]
                    height = img.size[1]
                    if width % 2 == 1:
                        width = width + 1
                    if height % 2 == 1:
                        height = height + 1
                    # print(width)
                    # print(height)
                    print(f"w: {width}, h: {height}")
                    img_type = 'png'
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                    img.save(dst, img_type)


def main(source):

    try:

        if '.png' in source:

            # reader = easyocr.Reader(['en'], gpu=True, detector=True, recognizer=True)
            #
            # # 使用 EasyOCR 识别图像中的文本
            # result = reader.readtext(source, batch_size=16, allowlist="0123456789:")
            #
            # # 输出识别结果
            # for detection in result:
            #     print("文本:", detection[1], "置信度:", detection[2])

            # 打开图片
            image = Image.open(source)

            # 使用 Tesseract OCR 识别图像中的数字和符号
            # result = pytesseract.image_to_string(image, lang='eng', config='--psm 13 --oem 1 -c tessedit_char_whitelist=0123456789:')

            # 输出识别结果
            # print("识别结果:", result)

            # 获取非空白像素的边界框
            bbox = image.getbbox()

            # 裁剪图像，去除空白像素
            trimmed_image = image.crop(bbox)

            trimmed_image.save(source)

            image = Image.open(source)
            # 获取图片的宽度和高度
            width, height = image.size

            # 更新最大宽度和最大高度
            max_width.append(width)
            max_height.append(height)

    except Exception as e:
        print(e)


def crop_image(source, target_width, target_height, alignment="center"):
    image = Image.open(source)

    if alignment == "top":
        left = 0
        top = 0
    elif alignment == "center":
        left = (image.width - target_width) // 2
        top = (image.height - target_height) // 2
    elif alignment == "bottom":
        left = 0
        top = image.height - target_height

    right = left + target_width
    bottom = top + target_height

    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save(source)

    image.close()


def fixNum(num):
    if num % 2 == 1:
        num += 1
    return num


# 判断传入文件夹或者多个文件
if len(preview_url) == 1:
    # 传入文件夹则偶数尺寸处理
    single_mode = 1
else:
    # 传入多个文件则取最大值处理
    single_mode = 0

if not single_mode:

    for k in range(len(preview_url)):
        main(preview_url[k])

    w = fixNum(max(max_width))
    h = fixNum(max(max_height))

    for k in range(len(preview_url)):
        # crop_image(preview_url[k], 112, 112, "center")
        crop_image(preview_url[k], w, h, "center")

    print(f"max_width: {max_width}, max_height: {max_height}")
    print(f"w: {w}, h: {h}")

else:
    for k in range(len(preview_url)):
        main_single(preview_url[k])
