import os.path
import sys
import imageio
import numpy as np
import time
import pygame
import xml.etree.ElementTree as ET

# 加载背景图片
from PIL import Image, ImageDraw


def generate_checkerboard(width, height, square_size, alpha=25):
    # 创建一个白色背景图像
    image = Image.new("RGBA", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # 计算每行和每列方格的数量
    squares_per_row = width // square_size
    squares_per_column = height // square_size

    # 绘制棋盘网格
    for i in range(squares_per_row):
        for j in range(squares_per_column):
            # 计算方格的左上角和右下角坐标
            x0 = i * square_size
            y0 = j * square_size
            x1 = x0 + square_size
            y1 = y0 + square_size

            # 根据方格的位置确定颜色和不透明度
            color = (255 - alpha, 255 - alpha, 255 - alpha, 255) if (i + j) % 2 == 0 else (255, 255, 255, 255)

            # 绘制方格
            draw.rectangle([x0, y0, x1, y1], fill=color)
    image.save(background_name)

    return image


# 初始化 Pygame
pygame.init()

# 设置初始屏幕尺寸和缩放比例
list_modes = pygame.display.list_modes()
# 设置初始屏幕缩放比例，数值越小，窗口越小
list_index = 6
screen_index = list_index if len(list_modes) >= list_index else min(len(list_modes) - 1, 0)
aspect_ratio = pygame.display.list_modes()[int(screen_index)][0] / 1080
# print(aspect_ratio)
initial_width = int(1080 // aspect_ratio)
initial_height = int(1920 // aspect_ratio)

current_w = pygame.display.Info().current_w
current_h = pygame.display.Info().current_h
initial_x = current_w // 2 * 0 - initial_width // 2
initial_y = current_h // 4 * 1 - initial_height // 2

# os.environ['SDL_VIDEO_CENTERED'] = '1'  # 设置窗口居中
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (initial_x,initial_y)
print(pygame.display.Info())
print(initial_x, initial_y, initial_width, initial_height)
# sys.exit()

display = pygame.RESIZABLE | pygame.SCALED | pygame.DOUBLEBUF
# display = pygame.RESIZABLE | pygame.SCALED | pygame.OPENGL
# display = pygame.RESIZABLE | pygame.SCALED | pygame.HWSURFACE
screen = pygame.display.set_mode((initial_width, initial_height), display)

# 设置标题
pygame.display.set_caption('MAML Preview')

# 准备录制
recording = False
frames = []

# 设置背景
background_name = 'grid.webp'
image = generate_checkerboard(1080, 1920, 10)
background_image = pygame.image.load(background_name)
# background_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)

# 定义颜色
TRANSPARENT = '#F9F9F9'
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 初始化时钟
clock = pygame.time.Clock()


def parse_color(color_value):
    try:
        return pygame.Color(color_value)
    except ValueError:
        if isinstance(color_value, tuple) and len(color_value) == 3:
            try:
                return pygame.Color(*color_value)
            except ValueError:
                pass
        if isinstance(color_value, str) and color_value.startswith('#'):
            try:
                return pygame.Color(color_value)
            except ValueError:
                pass
        raise ValueError(f"Invalid color value: {color_value}")


def get_fill_color_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    element = root.find('.//colorElement')
    if element is not None:
        fillColor = element.get('fillColor')
        if fillColor:
            try:
                return parse_color(fillColor)
            except ValueError as e:
                print(f"Invalid color value: {fillColor}")
                return RED  # 使用默认颜色或其他处理方式
    return RED  # 使用默认颜色或其他处理方式


def render_from_xml(xml_file, surface):

    # 示例：加载并解析XML文件（根据你的实际情况修改）
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for element in root.findall('.//Rectangle'):  # 假设存在矩形元素
        fillColor = element.get('fillColor')
        if fillColor:
            try:
                fillColor = parse_color(fillColor)
            except ValueError as e:
                print(f"Invalid color value: {fillColor}")
                fillColor = RED  # 使用默认颜色或其他处理方式

        x = int(element.get('x', 0))
        y = int(element.get('y', 0))
        w = int(element.get('width', 100))
        h = int(element.get('height', 100))
        cornerRadius = int(element.get('cornerRadius', 0))

        # 在虚拟表面上绘制矩形
        pygame.draw.rect(surface, fillColor, (x, y, w, h), border_radius=cornerRadius)
        # pygame.draw.rect(surface, (255, 0, 0), (320 - 25, 240 - 25, 50, 50))

    # 创建字体对象
    font_size = 48
    font = pygame.font.Font('/Users/wangshilong/Library/Fonts/HarmonyOS_Sans_SC_Medium.ttf', font_size)
    # font = pygame.font.Font('/Library/Fonts/SF-Pro.ttf', font_size)
    # 获取当前帧率
    fps = clock.get_fps()
    fps_str = f"#frame_rate: {fps:.2f}"
    # 渲染文本
    text = font.render(fps_str, True, '#0000ff')
    # 将文本绘制在左上角 (100, 100)
    surface.blit(text, (100, 100))
    fps_str = f"#time: {time.time() * 1000}"
    text = font.render(fps_str, True, '#0000ff')
    # 将文本绘制在左上角 (100, 100)
    surface.blit(text, (100, 200))


# 示例 XML 文件路径
xml_file = "./manifest.xml"

# 创建虚拟表面
virtual_surface = pygame.Surface((initial_width * aspect_ratio, initial_height * aspect_ratio))

# 主循环
running = True
is_paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # 更新窗口大小
            event_w = int(event.w)
            event_h = int(event.w / initial_width * initial_height)
            print(event_w, event_h)
            screen = pygame.display.set_mode((event_w, event_h), pygame.RESIZABLE | pygame.DOUBLEBUF)
            print(f"Window resized to ({event.w}, {event.h})")

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                # 截图并保存为文件
                pygame.image.save(capture_surface, "screenshot.png")
                print("Screenshot saved as screenshot.png")
            if event.key == pygame.K_SPACE:
                is_paused = not is_paused  # 切换暂停状态
                print("Pause:", is_paused)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # print(f"Mouse button down at ({x}, {y})")
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            print(f"Mouse motion at ({x}, {y})")
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            # print(f"Mouse button up at ({x}, {y})")

    # 缩放背景图片到当前窗口大小
    # scaled_background = pygame.transform.scale(background_image, (initial_width * aspect_ratio * 1.5, initial_height * aspect_ratio * 1.5))

    # 绘制缩放后的背景图片到屏幕上
    virtual_surface.blit(background_image, (0, 0))

    # 渲染内容到虚拟表面
    render_from_xml(xml_file, virtual_surface)
    # print(virtual_surface.get_size())

    # 缩放虚拟表面到当前窗口大小
    scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())

    # 绘制缩放后的表面到实际屏幕上
    screen.blit(scaled_surface, (0, 0))

    capture_surface = pygame.transform.scale(virtual_surface, (initial_width * aspect_ratio, initial_height * aspect_ratio))

    # 更新显示
    pygame.display.flip()

    if recording:
        # 捕获当前屏幕图像
        frame = pygame.surfarray.array3d(screen)
        frame = np.transpose(frame, (1, 0, 2))
        frames.append(frame)

    if not is_paused:
        pass
        # print(clock.get_fps())

    # 控制帧率
    clock.tick(60)

# 退出 Pygame
# print(clock.get_fps())
os.remove(background_name)
pygame.quit()
sys.exit()
