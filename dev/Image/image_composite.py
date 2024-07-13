import os
import sys

import pyperclip
from PIL import Image
import cv2
import numpy as np
from dev.Image.image_crop import crop_image


def composite_image(source_list, image_path='example.png'):
    # 读取图像
    images = [Image.open(filename) for filename in source_list]

    # 创建一个与第一张图像相同大小的新图像
    result = Image.new("RGBA", images[0].size)

    # 合并图像
    for image in images:
        result = Image.alpha_composite(result, image.convert("RGBA"))

    result.save(image_path)
    result = result.getbbox()
    return result[0], result[1], result[2] - result[0], result[3] - result[1]


def detect_edges_and_bbox(image_path):
    # 打开图像
    image = cv2.imread(image_path)

    # 使用Canny边缘检测
    edges = cv2.Canny(image, 100, 200)

    # 查找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 获取所有轮廓的组合边界框
    x_values = []
    y_values = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        x_values.append(x)
        x_values.append(x + w)
        y_values.append(y)
        y_values.append(y + h)

    # 计算包围所有边缘的大框
    x_min = min(x_values)
    x_max = max(x_values)
    y_min = min(y_values)
    y_max = max(y_values)

    # 绘制大框
    image_with_bbox = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.rectangle(image_with_bbox, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
    rect_points = [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)]
    # print(rect_points)
    # 将图像转换回PIL格式
    image_with_bbox_pil = Image.fromarray(image_with_bbox)

    # 显示结果
    # image_with_bbox_pil.show()
    image_with_bbox_pil.save('example_cv2.jpg')

    # 返回大框坐标
    return x_min - bleed, y_min - bleed, x_max - x_min + bleed * 2, y_max - y_min + bleed * 2


if __name__ == '__main__':

    # per side bleed
    bleed = 10
    source_list = pyperclip.paste().split('\n')
    _rename = 0
    _file = 'img_'
    _end = '.webp'
    if _rename:
        for fb in range(len(source_list)):
            os.rename(source_list[fb], os.path.join(os.path.dirname(source_list[fb]), _file + str(fb) + _end))
    print(source_list)

    result = composite_image(source_list)
    print("Simple boxes:", result)
    image_path = 'example.png'
    bbox_list = detect_edges_and_bbox(image_path)
    print("Bounding boxes:", bbox_list)
    for img in source_list:
        crop_image(img, bbox_list[0], bbox_list[1], bbox_list[2], bbox_list[3], quality=80)
        folder_name = os.path.dirname(img)
    os.rename(folder_name, str(folder_name + str(bbox_list)))
