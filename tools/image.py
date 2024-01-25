# import pytesseract
# import easyocr
import pyperclip
from PIL import Image


preview_url = pyperclip.paste().split('\n')
print(f'preview_url: {preview_url}')

max_width = []
max_height = []


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


for k in range(len(preview_url)):
    main(preview_url[k])

w = fixNum(max(max_width))
h = fixNum(max(max_height))
print(f"max_width: {max_width}, max_height: {max_height}")
print(f"w: {w}, h: {h}")

for k in range(len(preview_url)):
    # crop_image(preview_url[k], 798, 798, "center")
    crop_image(preview_url[k], w, h, "center")
