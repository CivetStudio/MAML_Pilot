import chunk
import time

from PIL import Image, ImageDraw


def add_black_border(image, chunk_info):
    # 获取图像大小
    width, height = image.size

    # 从 chunk_info 字典中获取边缘信息
    top = chunk_info.get('Top', (0, 0, 0))
    bottom = chunk_info.get('Bottom', (0, 0, 0))
    left = chunk_info.get('Left', (0, 0, 0))
    right = chunk_info.get('Right', (0, 0, 0))

    # 创建一个新的图像对象，大小为原图像加上黑边的大小
    new_width = width + 2
    new_height = height + 2
    new_image = Image.new('RGBA', (new_width, new_height), color=(0, 0, 0, 0))

    # 将原图像粘贴到新图像的合适位置
    new_image.paste(image, (1, 1))

    # 创建一个ImageDraw对象
    draw = ImageDraw.Draw(new_image)
    # 定义矩形的左上角和右下角坐标
    x0, y0 = 0, left[0]
    x1, y1 = 0, left[1]
    x2, y2 = width + 1, right[0]
    x3, y3 = width + 1, right[1]
    x4, y4 = top[0], 0
    x5, y5 = top[1], 0
    x6, y6 = bottom[0], height + 1
    x7, y7 = bottom[1], height + 1
    # 定义矩形的颜色
    rectangle_color = "black"
    # 在图像上绘制矩形
    draw.rectangle([x0, y0, x1, y1], fill=rectangle_color, outline=None)
    draw.rectangle([x2, y2, x3, y3], fill=rectangle_color, outline=None)
    draw.rectangle([x4, y4, x5, y5], fill=rectangle_color, outline=None)
    draw.rectangle([x6, y6, x7, y7], fill=rectangle_color, outline=None)
    return new_image


def main(input_path, output_path=None):

    if output_path is None:
        output_path = input_path
    with open(input_path, 'rb') as f:
        data = f.read()

    # Pass the image data to the from_png_file_data method
    chunk_info = chunk.main(input_path)

    if chunk_info != {}:
        # 加载图像
        image = Image.open(input_path)

        # 添加黑边
        new_image = add_black_border(image, chunk_info)

        # 显示新图像
        # new_image.show()

        # 保存图像
        new_image.save(output_path)
    else:
        print("No NinePatch chunk found in the PNG file.")


if __name__ == '__main__':
    # 使用示例
    input_path = "./test/myninepatch2.9.png"
    output_path = "./test/myninepatch3.9.png"
    main(input_path, output_path)
