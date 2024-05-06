from PIL import Image
import os
import numpy as np


def has_black_border(image_path, threshold=10):
    # 打开图像
    img = Image.open(image_path)
    # 转换为灰度图像
    gray_img = img.convert('L')
    # 转换为numpy数组
    gray_array = np.array(gray_img)
    # 使用阈值化方法将灰度图像转换为二值图像
    binary_array = np.where(gray_array < 128, 0, 255)
    # 计算每一行和每一列的像素值总和
    row_sum = np.sum(binary_array, axis=1)
    col_sum = np.sum(binary_array, axis=0)
    # 检查是否有行或列的总和小于阈值
    if (row_sum < threshold).any() or (col_sum < threshold).any():
        return True
    return False


def check_images_in_folder(folder_path):
    # 遍历文件夹中的所有图像文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            if has_black_border(image_path):
                print(f"{filename} has black border.")
            else:
                pass
                # print(f"{filename} does not have black border.")


# 检查文件夹中的图像是否存在黑边
folder_path = "./test"
check_images_in_folder(folder_path)
