import os
import time

import pyperclip
import subprocess
from PIL import Image, ImageSequence
from dev.Image.image_crop import crop_image


def extract_frames(input_file, output_dir, crop_image_v=1):
    """
    使用 ffmpeg 从 MOV 文件中提取帧
    """
    os.makedirs(output_dir, exist_ok=True)
    output_pattern = os.path.join(output_dir, 'frame_%04d.png')

    # Run ffprobe to get the frame rate from the MOV file
    ffprobe_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=avg_frame_rate', '-of', 'default=noprint_wrappers=1:nokey=1', input_file]
    ffprobe_output = subprocess.check_output(ffprobe_cmd, encoding='utf-8').strip()

    fps_numerator, fps_denominator = map(int, ffprobe_output.split('/'))  # Extract numerator and denominator
    fps = fps_numerator / fps_denominator  # Calculate the frame rate as a float value
    print(fps)
    cmd = ['ffmpeg', '-i', input_file, '-r', str(fps), output_pattern]  # Add the -r option with extracted fps
    subprocess.run(cmd)

    crop_image_v = 0
    if crop_image_v:
        # 获取输出目录中的所有 PNG 文件
        png_files = [os.path.join(output_dir, file) for file in os.listdir(output_dir) if file.endswith('.png')]

        # 对每个 PNG 文件执行裁剪操作
        for png_file in png_files:
            # crop_image(png_file, 372, 674, 884, 438, 80)
            crop_image(png_file, 116, 454, 1056, 942, 80)


def create_apng(input_dir, output_file):
    """
    使用 Pillow 创建 APNG 文件
    """
    frames = []
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith('.png'):
            frames.append(Image.open(os.path.join(input_dir, filename)))
    frames[0].save(output_file, save_all=True, append_images=frames[1:], optimize=True, duration=100, loop=1, compress_level=8)


def convert_mov_to_apng(input_file, output_file):
    """
    将 MOV 文件转换为 APNG 文件
    """
    temp_dir = input_file.split('.')[0]
    extract_frames(input_file, temp_dir)
    create_apng(temp_dir, output_file)
    # 删除临时帧文件夹
    # for filename in os.listdir(temp_dir):
    #     os.remove(os.path.join(temp_dir, filename))
    # os.rmdir(temp_dir)


def convert_all_mov_to_apng(input_dir):
    """
    将输入目录中的所有 MOV 文件转换为 APNG 文件
    """
    output_dir = input_dir  # 输出目录与输入目录相同
    for filename in os.listdir(input_dir):
        if filename.endswith('.mov') or filename.endswith('mp4'):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + '.png')
            convert_mov_to_apng(input_file, output_file)


if __name__ == "__main__":
    fps = 15
    input_dir = pyperclip.paste().strip()  # 从剪贴板中获取输入目录路径
    if os.path.isdir(input_dir):
        convert_all_mov_to_apng(input_dir)
    else:
        input_dir = input('Please Input Correct Path: ')
        # input_dir = input('输入目录后按回车继续: ')
        if os.path.isdir(input_dir):
            convert_all_mov_to_apng(input_dir)
        else:
            # print('\r错误: 请检查目录格式! ')
            print('\rError: Path is not exist! ')
