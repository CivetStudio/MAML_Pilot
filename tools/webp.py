import time

import pyperclip
from PIL import Image
import os


def convert_images_to_webp(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            # if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')):

                input_path = os.path.join(root, filename)
                file_index = filename.split('_')[1].split('.')[0]
                if int(file_index) % 2 == 0:
                    print(file_index)
                    os.remove(input_path)
                # breakpoint()

                else:
                    # 构建输入和输出文件的完整路径
                    relative_path = os.path.relpath(input_path, input_folder)
                    output_path = os.path.join(output_folder, os.path.splitext(relative_path)[0] + '.webp')

                    # 确保输出文件夹的子文件夹存在
                    output_subfolder = os.path.dirname(output_path)
                    if not os.path.exists(output_subfolder):
                        os.makedirs(output_subfolder)

                    # 打开图像并保存为 WebP 格式
                    img = Image.open(input_path)
                    # img_init = 'dt1_0.webp'
                    # img_last = 'dt1_22.webp'
                    # if filename == img_init or filename == img_last:
                    #     resize = 0
                    # else:
                    #     resize = 1
                    resize = 1
                    if resize:
                        width, height = img.size
                        image_compress_ratio = 720 / 1080 * 1
                        new_width = int(width * image_compress_ratio)
                        new_height = int(height * image_compress_ratio)
                        img = img.resize((new_width, new_height))
                        # image.size = width * image_compress_ratio, height * image_compress_ratio
                        # image.save(_file_path)

                    img.save(output_path, 'webp')

                    print(f"Converted {relative_path} to {os.path.basename(output_path)}")

                    # 删除原始文件
                    if not input_path.endswith('.webp'):
                        os.remove(input_path)
                        print(f"Removed original file: {relative_path}")


# 替换为你的输入和输出文件夹路径
input_folder_path = pyperclip.paste()

# 执行转换
try:
    convert_images_to_webp(input_folder_path, input_folder_path)
except Exception as e:
    print(f"Exception: {e}")
