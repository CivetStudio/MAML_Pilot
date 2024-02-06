from PIL import Image
import os


def convert_images_to_webp(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                # 构建输入和输出文件的完整路径
                input_path = os.path.join(root, filename)
                relative_path = os.path.relpath(input_path, input_folder)
                output_path = os.path.join(output_folder, os.path.splitext(relative_path)[0] + '.webp')

                # 确保输出文件夹的子文件夹存在
                output_subfolder = os.path.dirname(output_path)
                if not os.path.exists(output_subfolder):
                    os.makedirs(output_subfolder)

                # 打开图像并保存为 WebP 格式
                img = Image.open(input_path)
                width, height = img.size
                image_compress_ratio = 1 + 0 * 720 / 1080
                new_width = int(width * image_compress_ratio)
                new_height = int(height * image_compress_ratio)
                new_width = 1440
                new_height = 1440
                img = img.resize((new_width, new_height))
                # image.size = width * image_compress_ratio, height * image_compress_ratio
                # image.save(_file_path)

                img.save(output_path, 'webp')

                print(f"Converted {relative_path} to {os.path.basename(output_path)}")

                # 删除原始文件
                os.remove(input_path)
                print(f"Removed original file: {relative_path}")


# 替换为你的输入和输出文件夹路径
input_folder_path = '/Users/wangshilong/Downloads/gif'

# 执行转换
try:
    convert_images_to_webp(input_folder_path, input_folder_path)
except Exception as e:
    print(f"Exception: {e}")
