from PIL import Image, ImageDraw
import math
import os

# 这是一个Python脚本，用于生成带描边的圆环图片，并将其保存为PNG文件。以下是代码的简要说明：

# 导入PIL模块中的Image和ImageDraw类
# 定义一些输入参数，例如圆环数量，图片名称，描边颜色，描边宽度等等。
# 计算圆环的半径和中心点，以及缩放后的图片的宽度和高度。
# 使用Image.new()函数创建一个空白的RGBA图像。
# 使用ImageDraw.Draw()函数创建一个可以用于绘制图像的对象。
# 使用一个for循环，通过调用draw.arc()函数来绘制每一个圆环。startAngle和arc_num参数控制了每个圆环的起始和终止角度。
# 通过计算圆弧的起始点和结束点的坐标，再通过draw.ellipse()函数来绘制圆弧的两个端点。
# 使用img.save()函数将生成的PNG图像保存到本地磁盘上。
# 使用os.listdir()函数遍历文件夹中的所有PNG图像文件，然后使用Image.open()函数打开每个PNG图像。
# 使用img.resize()函数将每个PNG图像缩放到指定大小，并使用img.save()函数保存缩放后的PNG图像。

# 输入参数
arc_num = 20  # 圆环数量
stroke_color = '#ffa902'  # 描边颜色，输入6位hex值
stroke_width = 22 * 2  # 描边宽度 w * 2
startAngle = -90  # startAngle 单位为度数，表示圆环的覆盖角度
direct = -1  # 1：顺时针 -1：逆时针
real_width = 80  # 圆环宽度
real_height = 80  # 圆环高度
filename = 'circle'  # 图片名称

# 内部变量
width = int(real_width * 2 + 2 * stroke_width)  # 处理时图像宽度
height = int(real_height * 2 + 2 * stroke_width)  # 处理时图像高度
stroke_style = 'inner'  # 描边样式: 内描边

# 计算圆环的半径和中心点
radius = min(width, height) / 2 - stroke_width / 2
radius2 = min(width, height) / 2 - stroke_width * 1.5
center = (width / 2, height / 2)

# 生成圆环
img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

for i in range(arc_num + 1):
    draw.arc((
        center[0] - radius + stroke_width / 2, center[1] - radius + stroke_width / 2,
        center[0] + radius - stroke_width / 2,
        center[1] + radius - stroke_width / 2),
        start=startAngle,
        end=startAngle + i / arc_num * 360,
        fill=stroke_color,
        width=stroke_width)

    # specify the start and end angles of the arc in degrees
    start_angle = startAngle
    end_angle = startAngle + i / arc_num * 360

    # calculate the start and end points of the arc
    start_x = center[0] + radius2 * math.cos(math.radians(start_angle))
    start_y = center[1] + radius2 * math.sin(math.radians(start_angle))
    end_x = center[0] + radius2 * math.cos(math.radians(end_angle))
    end_y = center[1] + radius2 * math.sin(math.radians(end_angle))

    draw.ellipse((start_x - stroke_width / 2 + 1, start_y - stroke_width / 2 + 1, start_x + stroke_width / 2 - 1,
                  start_y + stroke_width / 2 - 1), fill=stroke_color)
    draw.ellipse((end_x - stroke_width / 2 + 1, end_y - stroke_width / 2 + 1, end_x + stroke_width / 2 - 1,
                  end_y + stroke_width / 2 - 1), fill=stroke_color)

    img.save(f"{filename}_{i}.png")

# 放大2x缩小可去除锯齿
for filename in os.listdir('./'):
    if filename.endswith('.png'):
        # 打开原始图片
        with Image.open('./' + filename) as img:
            # 缩放图片
            img = img.resize((int(real_width + stroke_width - 2), int(real_width + stroke_width - 2)))
            # img = img.resize((int(real_width + stroke_width - 2), int(real_width + stroke_width - 2)), Image.LANCZOS)
            # 保存缩放后的图片
            if direct == -1:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            img.save('./' + filename)
