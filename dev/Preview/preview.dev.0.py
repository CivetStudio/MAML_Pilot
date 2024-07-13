import pygame

# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸
screen_width = pygame.display.list_modes()[0][0] // 4
screen_height = pygame.display.list_modes()[0][1] // 4
screen = pygame.display.set_mode((screen_width, screen_height))
print(pygame.display.list_modes())

# 设置标题
pygame.display.set_caption('Pygame 动画矩形示例')

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 定义矩形的初始位置和速度
rect_x = 50
rect_y = 50
rect_width = 100
rect_height = 50
rect_speed_x = 5
rect_speed_y = 5

# 初始化时钟
clock = pygame.time.Clock()

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新矩形的位置
    rect_x += rect_speed_x
    rect_y += rect_speed_y

    # 碰撞检测并反转速度
    if rect_x < 0 or rect_x + rect_width > screen_width:
        rect_speed_x = -rect_speed_x
    if rect_y < 0 or rect_y + rect_height > screen_height:
        rect_speed_y = -rect_speed_y

    # 清空屏幕
    screen.fill(WHITE)

    # 绘制矩形
    pygame.draw.rect(screen, RED, (rect_x, rect_y, rect_width, rect_height))

    # 更新显示
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)
    # print(clock.get_fps())
    # print(clock.tick_busy_loop())

# 退出 Pygame
pygame.quit()
