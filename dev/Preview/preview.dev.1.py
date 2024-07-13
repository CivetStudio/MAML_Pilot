import pygame
import sys

# 初始化 Pygame
pygame.init()

# 设置窗口尺寸和标志
screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE | pygame.DOUBLEBUF)
pygame.display.set_caption("MultiLine Text Height Example")

# 设置字体
font_size = 24
font = pygame.font.Font(None, font_size)

# 要显示的多行中文文本
multiline_text = "This is a long text that will be split into multiple lines. " \
                 "Pygame is a set of Python modules designed for writing video games. " \
                 "It includes computer graphics and sound libraries."

# 将中文文本拆分成多行
def split_text(text, font, max_width):
    lines = []
    current_line = ""
    for char in text:
        test_line = current_line + char
        text_width, _ = font.size(test_line)
        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = char
    lines.append(current_line)
    return lines

# 将中文文本拆分成多行
max_width = 600
lines = split_text(multiline_text, font, max_width)

# 计算文本高度
sacping_mult = 15 / 10
line_height = font.get_linesize() * sacping_mult
# line_height = font_size + 5  # 行高包括间距
text_height = len(lines) * line_height
print("总文本高度:", text_height)

# 获取文本在特定字体下的宽度和高度
text = "Hello, Pygame!"
text_width, text_height = font.size(text)
print("文本宽度:", font.size(text))


# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充屏幕背景颜色
    screen.fill((0, 0, 0))

    # 渲染并显示每一行文本
    y = 50  # 初始 y 坐标
    for line in lines:
        text_surface = font.render(line, True, (0, 255, 0))
        screen.blit(text_surface, (20, y))
        y += line_height

    # 更新显示
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
sys.exit()
