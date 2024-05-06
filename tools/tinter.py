import pyperclip
from PIL import Image
import os


def tint_images_color(input_folder_path, output_folder_path, color="#ffff00", keep_alpha=True):
    """
    将指定文件夹中的所有图像转换为指定颜色。

    参数:
    - input_folder_path: 输入文件夹路径，包含待处理的图像文件。
    - output_folder_path: 输出文件夹路径，保存处理后的图像文件。
    - color: 要应用的颜色，格式为十六进制字符串，例如"#ff0000"表示红色，默认为黄色("#ffff00")。
    - keep_alpha: 是否保留图像的 Alpha 通道，默认为 True。

    返回:
    无返回值，处理后的图像文件保存在输出文件夹中。
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder_path):
        input_file_path = os.path.join(input_folder_path, filename)
        output_file_path = os.path.join(output_folder_path, filename)

        # 判断文件是否为图像文件
        if os.path.isfile(input_file_path) and any(
                input_file_path.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
            # 打开图像文件
            image = Image.open(input_file_path)

            # 转换图像颜色
            if keep_alpha:
                image = image.convert("RGBA")
            else:
                image = image.convert("RGB")

            pixels = image.load()
            width, height = image.size
            for x in range(width):
                for y in range(height):
                    r, g, b, a = pixels[x, y]
                    if a > 0:
                        pixels[x, y] = tuple(int(color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)) + (a,)

            # 保存处理后的图像文件
            image.save(output_file_path)
            print(f"Processed {input_file_path} -> {output_file_path}")


# 测试代码
if __name__ == "__main__":
    input_folder = pyperclip.paste()
    output_folder = input_folder
    tint_images_color(input_folder, output_folder, color="#111111", keep_alpha=True)
