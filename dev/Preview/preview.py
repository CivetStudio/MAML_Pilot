import pygame
import threading
import os
import sys
import time
import datetime
from PIL import Image
from bs4 import BeautifulSoup
from dev.Refactor.functions import *
from dev.Refactor.refactor import *

simulation_screen_width = 1080
simulation_screen_height = 1920
Var = {}

time_sys = str(int(time.time() * 1000))
day_of_week = int(datetime.datetime.fromtimestamp(int(time_sys) / 1000).weekday() + 2) % 7
day_of_week = 7 if day_of_week == 0 else day_of_week

Var['System'] = {
    # 触摸
    '#touch_x': 0,
    '#touch_y': 0,
    '#touch_begin_x': 0,
    '#touch_begin_y': 0,
    '#touch_begin_time': 0,
    # 屏幕
    '#screen_width': simulation_screen_width,
    '#screen_height': simulation_screen_height,
    '#view_width': 0,
    '#view_height': 0,
    '#raw_screen_width': simulation_screen_width,
    '#raw_screen_height': simulation_screen_height,
    '#view_x': 0,
    '#view_y': 0,
    # 日期
    '#time': int(int(time_sys) / 1000),
    '#time_sys': time_sys,
    '#year': int(formatDate('yyyy', time_sys)),
    '#month': int(int(formatDate('M', time_sys)) - 1 + 12) % 12,
    '#month1': int(formatDate('M', time_sys)),
    '#date': int(formatDate('d', time_sys)),
    '#day_of_week': day_of_week,
    '#day_of_week-1': day_of_week - 1,
    '#hour12': int(formatDate('h', time_sys)),
    '#hour24': int(formatDate('H', time_sys)),
    '#minute': int(formatDate('m', time_sys)),
    '#second': int(formatDate('s', time_sys)),
    '#ampm': 0 if int(formatDate('H', time_sys)) < 12 else 1,
    '#time_format': 0,
}

con = {
    'number': '#',
    'string': '@'
}


# 定义更新字典的函数
def update_var_system():
    while True:
        time_sys = str(int(time.time() * 1000))

        day_of_week = int(datetime.datetime.fromtimestamp(int(time_sys) / 1000).weekday() + 2) % 7
        day_of_week = 7 if day_of_week == 0 else day_of_week

        Var['System'].update({
            # 触摸
            '#touch_x': 0,
            '#touch_y': 0,
            '#touch_begin_x': 0,
            '#touch_begin_y': 0,
            '#touch_begin_time': 0,
            # 屏幕
            '#screen_width': simulation_screen_width,
            '#screen_height': simulation_screen_height,
            '#view_width': 0,
            '#view_height': 0,
            '#raw_screen_width': simulation_screen_width,
            '#raw_screen_height': simulation_screen_height,
            '#view_x': 0,
            '#view_y': 0,
            # 日期
            '#time': int(int(time_sys) / 1000),
            '#time_sys': time_sys,
            '#year': int(formatDate('yyyy', time_sys)),
            '#month': int(int(formatDate('M', time_sys)) - 1 + 12) % 12,
            '#month1': int(formatDate('M', time_sys)),
            '#date': int(formatDate('d', time_sys)),
            '#day_of_week': day_of_week,
            '#day_of_week-1': day_of_week - 1,
            '#hour12': int(formatDate('h', time_sys)),
            '#hour24': int(formatDate('H', time_sys)),
            '#minute': int(formatDate('m', time_sys)),
            '#second': int(formatDate('s', time_sys)),
            '#ampm': 0 if int(formatDate('H', time_sys)) < 12 else 1,
            '#time_format': 0,
        })

        # 按键的长度从长到短排序
        Var['System'] = dict(sorted(Var['System'].items(), key=lambda item: len(item[0]), reverse=True))

        # 打印当前更新的字典（可选）
        # print(Var['System'])

        # 等待1毫秒
        time.sleep(0.001)


# 获取用户屏幕信息
def get_user_ratio(view_height):
    pygame.init()
    info = pygame.display.Info()
    usr_current_h = info.current_h
    usr_dpi_ratio = usr_current_h * 0.9 / view_height
    pygame.quit()
    return usr_dpi_ratio


def is_hex_color(value):
    hex_pattern = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')
    return bool(hex_pattern.match(value))


def eval_safe(value):
    try:
        result = eval(value)
        if re.search(r'["(", ")"]', str(result)):
            result = eval_safe(result)
    except Exception as e:
        result = value
    return result


def fix_var_dict(User, var_pre='#'):
    for key, value in User.items():
        pattern = fr'{var_pre}\w+\b'
        re_var = re.search(pattern, str(value))
        if re_var:
            re_var_name = re_var.group()
            User[key] = eval_safe(str(User[key]))
            if not is_hex_color(re_var_name):
                if re_var_name in Var['System']:
                    print(re_var_name)
                    print('Has System Block')
                else:
                    User[key] = value.replace(str(re_var_name), str(User[re_var_name]))
                User[key] = eval_safe(str(User[key]))
                fix_var_dict(User, '@')
                for _key, _value in User.items():
                    pattern = fr'{var_pre}\w+\b'
                    re_var = re.search(pattern, str(value))
                    if re_var:
                        fix_var_dict(User)
    return User


def parse_color(color_value):
    try:
        return pygame.Color(color_value)
    except ValueError:
        # 尝试解析 RGB 三元组
        if isinstance(color_value, tuple) and len(color_value) == 3:
            try:
                return pygame.Color(*color_value)
            except ValueError:
                pass
        # 尝试解析十六进制字符串
        if isinstance(color_value, str) and color_value.startswith('#'):
            try:
                return pygame.Color(color_value)
            except ValueError:
                pass
        raise ValueError(f"Invalid color value: {color_value}")


# 解析表达式
def parse_expression(value):
    try:
        target_value = Var['User'][value]
        # if re.search(r'[#@]', Var['User'][value]):
        #     target_value = parse_expression(Var['User'][value])
        parse_result = eval(str(target_value))
        if re.search(r'[#@]', parse_result):
            parse_result = parse_expression(parse_result)
    except Exception as e:
        parse_result = value
        # print(e)
    return parse_result


def parse_soup(xml_file):

    soup = BeautifulSoup(open(xml_file), 'lxml-xml')
    var_from_target = get_xml_variable(xml_file)
    Var['User'] = {}
    for v in range(len(var_from_target)):
        for vft_tag in soup.find_all('Var'):
            vft_name = vft_tag.get('name')
            vft_exp = vft_tag.get('expression')
            vft_exp = parse_expression(vft_exp)
            vft_type = vft_tag.get('type', 'number')
            vft = con[vft_type] + str(var_from_target[v])
            if vft_name == var_from_target[v]:
                # print(vft_tag)
                Var['User'][vft] = vft_exp
    # print(var_from_target)
    Var['User'] = fix_var_dict(Var['User'])
    # print(Var['User'])
    # print(Var['System'])

    manifest_root = soup.find_all(True)[0].name

    for tags in soup.find_all():
        if tags.name not in ['Var']:
            for _attr, _exp in tags.attrs.items():
                for _sys, _sys_val in Var['System'].items():
                    tags[_attr] = str(tags[_attr]).replace(str(_sys), str(_sys_val))
                    for _user, _user_val in Var['User'].items():
                        tags[_attr] = str(tags[_attr]).replace(str(_user), str(_user_val))
                        tags[_attr] = eval_safe(tags[_attr])
                        _exp = tags[_attr]

    return soup


def render_from_xml(xml_file, screen_width, screen_height, scale_factor=1):
    global Var, screen

    soup = parse_soup(xml_file)
    for element in soup.find_all():
        if element.name == "Rectangle":
            x = parse_expression(element.get("x", 0))
            y = parse_expression(element.get("y", 0))
            w = parse_expression(element.get("w", 1))
            h = parse_expression(element.get("h", 1))

            fillColor = element.get("fillColor", "#00ff00")
            fillColor = parse_color(fillColor)

            cornerRadius = int(element.get("cornerRadius", "0"))

            if element.get("align", None) == "center":
                x = x - w / 2
            elif element.get("align", None) == "right":
                x = x - w

            if element.get("alignV", None) == "center":
                y = y - h / 2
            elif element.get("alignV", None) == "bottom":
                y = y - h

            x = int(x * scale_factor)
            y = int(y * scale_factor)
            w = int(w * scale_factor)
            h = int(h * scale_factor)
            print(x, y, w, h)

            pygame.draw.rect(screen, fillColor, (x, y, w, h), border_radius=cornerRadius)
        elif element.name == "Image":
            src = element["src"]
            src = os.path.join(os.path.dirname(xml_file), src)
            image = Image.open(src)
            bmp_width = image.width
            bmp_height = image.height

            x = parse_expression(element.get("x", 0))
            y = parse_expression(element.get("y", 0))
            w = parse_expression(element.get("w", bmp_width))
            h = parse_expression(element.get("h", bmp_height))

            align = element.get("align", "left")
            alignV = element.get("alignV", "top")

            if align == "center":
                x = x - w / 2
            elif align == "right":
                x = x - w

            if alignV == "center":
                y = y - h / 2
            elif alignV == "bottom":
                y = y - h

            x = int(x * scale_factor)
            y = int(y * scale_factor)
            w = int(w * scale_factor)
            h = int(h * scale_factor)

            image = pygame.image.load(src)
            image = pygame.transform.scale(image, (int(w), int(h)))
            screen.blit(image, (int(x), int(y)))
        elif element.name == "Text":
            x = parse_expression(element.get("x", 0))
            y = parse_expression(element.get("y", 0))
            size = int(element["size"])

            color = element.get("color", "#00ff00")
            color = pygame.Color(color)
            text = str(element.get("text", "")).encode('utf-8')
            print(text)

            align = element.get("align", "left")
            alignV = element.get("alignV", "top")

            font = pygame.font.Font("/Users/wangshilong/Library/Fonts/HarmonyOS_Sans_SC_Medium.ttf", size)
            text_surface = font.render(text, True, color)

            text_width = int(text_surface.get_width() * 1)
            text_height = int(text_surface.get_height() * 1)

            if align == "center":
                x = x - text_width / 2
            elif align == "right":
                x = x - text_width

            if alignV == "center":
                y = y - text_height / 2
            elif alignV == "bottom":
                y = y - text_height

            x = int(x * scale_factor)
            y = int(y * scale_factor)
            size = int(size * scale_factor)

            print(x, y, size)

            font = pygame.font.Font("/Users/wangshilong/Library/Fonts/HarmonyOS_Sans_SC_Medium.ttf", size)
            text_surface = font.render(text, True, color)

            screen.blit(text_surface, (x, y))

    pygame.display.flip()

    # 截图
    if screen_cap:
        pygame.image.save(screen, "screenshot.png")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        soup = parse_soup(xml_file)
        for element in soup.find_all():
            if element.name == "Rectangle":
                x = parse_expression(element.get("x", 0))
                y = parse_expression(element.get("y", 0))
                w = parse_expression(element.get("w", 1))
                h = parse_expression(element.get("h", 1))

                fillColor = element.get("fillColor", "#00ff00")
                fillColor = parse_color(fillColor)

                cornerRadius = int(element.get("cornerRadius", "0"))

                if element.get("align", None) == "center":
                    x = x - w / 2
                elif element.get("align", None) == "right":
                    x = x - w

                if element.get("alignV", None) == "center":
                    y = y - h / 2
                elif element.get("alignV", None) == "bottom":
                    y = y - h

                x = int(x * scale_factor)
                y = int(y * scale_factor)
                w = int(w * scale_factor)
                h = int(h * scale_factor)
                print(x, y, w, h)

                pygame.draw.rect(screen, fillColor, (x, y, w, h), border_radius=cornerRadius)
            elif element.name == "Image":
                src = element["src"]
                src = os.path.join(os.path.dirname(xml_file), src)
                image = Image.open(src)
                bmp_width = image.width
                bmp_height = image.height

                x = parse_expression(element.get("x", 0))
                y = parse_expression(element.get("y", 0))
                w = parse_expression(element.get("w", bmp_width))
                h = parse_expression(element.get("h", bmp_height))

                align = element.get("align", "left")
                alignV = element.get("alignV", "top")

                if align == "center":
                    x = x - w / 2
                elif align == "right":
                    x = x - w

                if alignV == "center":
                    y = y - h / 2
                elif alignV == "bottom":
                    y = y - h

                x = int(x * scale_factor)
                y = int(y * scale_factor)
                w = int(w * scale_factor)
                h = int(h * scale_factor)

                image = pygame.image.load(src)
                image = pygame.transform.scale(image, (int(w), int(h)))
                screen.blit(image, (int(x), int(y)))
            elif element.name == "Text":
                x = parse_expression(element.get("x", 0))
                y = parse_expression(element.get("y", 0))
                size = int(element["size"])

                color = element.get("color", "#00ff00")
                color = pygame.Color(color)
                text = str(element.get("text", "")).encode('utf-8')
                print(text)

                align = element.get("align", "left")
                alignV = element.get("alignV", "top")

                font = pygame.font.Font("/Users/wangshilong/Library/Fonts/HarmonyOS_Sans_SC_Medium.ttf", size)
                text_surface = font.render(text, True, color)

                text_width = int(text_surface.get_width() * 1)
                text_height = int(text_surface.get_height() * 1)

                if align == "center":
                    x = x - text_width / 2
                elif align == "right":
                    x = x - text_width

                if alignV == "center":
                    y = y - text_height / 2
                elif alignV == "bottom":
                    y = y - text_height

                x = int(x * scale_factor)
                y = int(y * scale_factor)
                size = int(size * scale_factor)

                print(x, y, size)

                font = pygame.font.Font("/Users/wangshilong/Library/Fonts/HarmonyOS_Sans_SC_Medium.ttf", size)
                text_surface = font.render(text, True, color)

                screen.blit(text_surface, (x, y))

        pygame.display.flip()

        # 控制帧率
        clock.tick(60)  # 每秒最多60帧
    pygame.quit()


if __name__ == "__main__":
    xml_file = './../su/manifest.xml'
    xml_file = './manifest.xml'
    # xml_file = '/Volumes/T7/Theme Client/叮咚叮咚/3D简约郁金香/国内版/OPPO/lockscreen/advance/manifest.xml'
    view_width = simulation_screen_width  # 宽度设定为800
    view_height = simulation_screen_height  # 高度设定为600
    view_ratio = get_user_ratio(view_height) * 0.8
    screen_cap = 1
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # 设置窗口居中

    # 启动一个后台线程来更新字典
    update_thread = threading.Thread(target=update_var_system)
    update_thread.daemon = True  # 设置为守护线程，这样主程序退出时该线程也会退出
    update_thread.start()

    # 主线程可以继续做其他事情
    try:
        while True:
            # 主线程在这里可以执行其他操作
            # 这里我们只是等待一段时间，观察字典的更新情况
            time.sleep(1)

            pygame.init()
            scale_factor = view_ratio
            initial_width = int(view_width * scale_factor)
            initial_height = int(view_height * scale_factor)
            screen = pygame.display.set_mode((initial_width, initial_height), pygame.RESIZABLE)
            pygame.display.set_caption('Pygame 实时渲染示例')
            clock = pygame.time.Clock()

            virtual_surface = pygame.Surface((initial_width, initial_height))

            # 缩放虚拟表面到当前窗口大小
            scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())

            # 绘制缩放后的表面到实际屏幕上
            screen.blit(scaled_surface, (0, 0))

            # 更新显示
            pygame.display.flip()

            # 控制帧率
            clock.tick(60)

            render_from_xml(xml_file, view_width, view_height)

    except KeyboardInterrupt:
        print("程序结束")
