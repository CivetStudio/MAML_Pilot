import pygame
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import sys

# 初始化 Pygame
pygame.init()

# 设置窗口尺寸
screen = pygame.display.set_mode((640, 480))

# 设置字体
font_size = 36
font = ImageFont.truetype("/Users/wangshilong/Library/Fonts/HarmonyOS_Sans_SC_Medium.ttf", font_size)

# 创建文本图像
text = "Hello, Pygame!"
text_width, text_height = font.getsize(text)
image_width = text_width + 10 * 4 # 添加一些额外的空间
image_height = text_height + 10 * 4  # 添加一些额外的空间
image = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)
draw.text((5 * 4, 5 * 4), text, font=font, fill=(0, 255, 0))

# 创建阴影效果
shadow_offset = (3, 10)
radius = 3
shadow = image.filter(ImageFilter.GaussianBlur(radius))  # 添加模糊效果
shadow = ImageChops.offset(shadow, *shadow_offset)
shadow = Image.alpha_composite(Image.new("RGBA", image.size, (0, 0, 0, 0)), shadow)

# 将图像转换为 Pygame Surface 对象
image_surface = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
shadow_surface = pygame.image.fromstring(shadow.tobytes(), shadow.size, shadow.mode)

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充屏幕背景颜色
    screen.fill((0, 0, 0))

    # 绘制阴影效果
    screen.blit(shadow_surface, shadow_surface.get_rect())

    # 绘制原始文本
    screen.blit(image_surface, image_surface.get_rect())

    # 更新显示
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
sys.exit()
