import os.path
import random
import string
import sys
import zlib

import numpy as np
import psd_tools
from PIL import Image, ImageFilter
from psd_tools import PSDImage
from bs4 import BeautifulSoup
import re
from dev.Image.image_crop import crop_image
import subprocess

birth_day = '2024-05-10'
GREEN = '\033[92'
maml_tag_name = 'Lockscreen'
maml_sample_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<{maml_tag_name} frameRate="240" screenWidth="1080" version="1" vibrate="false" _dev="civet" _devTime="$_devTime" _splitExt="1" _splitGroup="1" _preload="1" _getSource="0" _pauseIntent="1" compiler="true" >

</{maml_tag_name}>
"""


def tn(n):
    # 如果你想输出 \t\t\t，你可以直接写成 f"\\t\\t\\t"，不需要变量 n
    _num_ = 0
    result = ''
    while _num_ <= n:
        result = result + '\t'
        _num_ += 1
    return result


def has_transparency(img):
    if img.mode == 'RGBA':
        transparent_pixels = any(pixel[3] < 255 for pixel in img.getdata())
        return transparent_pixels
    return False


_final_color_ = []
_final_color_e_ = []


def _layer_num(layer, _layer_num=0):
    # 检查图层与组的嵌套数量
    while str(layer.parent.name).upper() != 'ROOT':
        if layer.parent:
            layer = layer.parent
            _layer_num += 1
    return _layer_num


def _layer_loop(layer, _num_):
    # 通过嵌套数量来取得相应颜色值 -> 列表切片
    while str(layer.parent.name).upper() != 'ROOT':
        layer_ori = layer
        layer = layer.parent
        if layer.has_effects():
            _final_ = rgb_to_hex(parse_dict_color(layer.effects[0].color))
        else:
            _final_ = '###'
        _final_color_.append(_final_)
        _final_color_e_.append(layer.has_effects())
    _final_color_new_ = _final_color_[-_num_:]
    _final_color_e_new = _final_color_e_[-_num_:]
    _final_color_new = [_final_color_new_[i] for i in range(len(_final_color_new_)) if _final_color_e_new[i]]
    return _final_color_new


def find_overlay_color(layer, color_ori):
    _color_def = [color_ori]
    # 查找自身颜色叠加
    if layer.has_effects():
        _final_ = rgb_to_hex(parse_dict_color(str(layer.effects[0].color)))
        _color_def[0] = _final_

    # 查找父元素颜色叠加
    _layer_num_ = _layer_num(layer)
    _color_grp = _layer_loop(layer, _layer_num_)
    _color_ovl = _color_def + _color_grp
    layer.color = _color_ovl[-1]
    return layer.color


# def parse_color_overlay(layer, _e_color_=[]):
#     if str(layer.parent.name).upper() != 'ROOT':
#         effects_parent_color = get_parent_color(layer)
#         if effects_parent_color:
#             _e_color_.append(effects_parent_color[0])
#         if layer.parent and layer.parent.is_group():
#             layer = layer.parent
#             parse_color_overlay(layer)
#     else:
#         effects_parent_color = get_parent_color(layer)
#         if effects_parent_color:
#             _e_color_.append(effects_parent_color[0])
#     return _e_color_, max(len(_e_color_) - 1, 0)
#
#
# def color_overlay(origin_color_hex, overlay_color_hex, origin_color_opacity=100, overlay_color_opacity=100):
#     if overlay_color_hex:
#         origin_color_hex = origin_color_hex[1:]
#         overlay_color_hex = overlay_color_hex[1:]
#         if origin_color_opacity != overlay_color_opacity:
#             # 将十六进制颜色转换为RGB值
#             origin_color_rgb = tuple(int(origin_color_hex[i:i+2], 16) for i in (0, 2, 4))
#             overlay_color_rgb = tuple(int(overlay_color_hex[i:i+2], 16) for i in (0, 2, 4))
#
#             # 计算叠加后的颜色值
#             overlay_factor = overlay_color_opacity / 100
#             origin_factor = origin_color_opacity / 100
#             result_color_rgb = tuple(int((overlay_factor * overlay_channel + origin_factor * origin_channel) / (overlay_factor + origin_factor))
#                                      for overlay_channel, origin_channel in zip(overlay_color_rgb, origin_color_rgb))
#
#             # 返回叠加后的颜色值
#             return rgb_to_hex(result_color_rgb)
#         else:
#             return f'#{overlay_color_hex}'
#     else:
#         return f'#{origin_color_hex}'
#

def get_parent_color(layer):
    if layer.has_effects():
        try:
            for color in range(len(layer.effects)):
                if str(layer.effects[color]) == 'ColorOverlay':
                    effects_opacity = layer.effects[color].opacity
                    effects_color = rgb_to_hex(str(layer.effects[color].color))
                    # print(f"{tn(n)}颜色叠加: {effects_color}, {effects_opacity}%")
                    return effects_color, effects_opacity
        except Exception as e:
            print(e)
            return None
    else:
        return None


def add_parent_tag(soup, tag, layer):
    for _parent in soup.find_all('Group'):
        layer_alias = _parent.get('alias')
        if layer.parent.name and layer_alias == layer.parent.name:
            _parent.append(tag)
            # print('_parent:', _parent)


def is_pure_chinese(text):
    # 使用正则表达式匹配字符串是否只包含中文字符
    pattern = re.compile(r'^[\u4e00-\u9fa5]+$')
    return bool(pattern.match(text))


def contains_no_digits(text):
    # 使用正则表达式匹配字符串是否不包含数字
    pattern = re.compile(r'^\D+$')
    return bool(pattern.match(text))


def match_digits(text):
    # 定义匹配模式
    pattern = re.compile(r'\d+')
    # 将匹配到的数字替换为 %d
    new_text = pattern.sub(r'%d', text)
    return new_text


def match_weekday(text):
    # 定义匹配模式
    pattern = re.compile(r'(星期|周)[一二三四五六日]')
    # 查找匹配的字符串
    match = pattern.search(text)
    if match:
        # 查找匹配的字符串
        if text.startswith('星期'):
            new_text = pattern.sub(rf'{"E" * 4}', text)
        else:
            new_text = pattern.sub(rf'{"E" * len(match.group())}', text)
        return new_text
    else:
        return None


def is_pure_text(text):
    return is_pure_chinese(text) and contains_no_digits(text)


def custom_encrypt(input_string, m='m', crc32_mode=1):
    if crc32_mode:
        alias_dom_concat = m + hex(zlib.crc32(str(input_string).encode('UTF-8')))[2:].capitalize()
        alias_dom_hex = m if len(alias_dom_concat) == 8 else ''
        alias_str_new = str(alias_dom_concat + alias_dom_hex)
        return alias_str_new


def random_str(length):
    result = ''
    characters = string.ascii_letters + string.digits
    characters_length = len(characters)

    for i in range(length):
        random_index = random.randint(0, characters_length - 1)
        result += characters[random_index]

    return result


def parse_corner_radius(origination):
    try:
        corner_radius = -1
        origination = eval(str(origination))
        if type(origination) is dict:
            try:
                if origination[b'topRight'] == origination[b'topLeft'] == origination[b'bottomLeft'] == origination[b'bottomRight']:
                    corner_radius = origination[b'topRight']
            except Exception as e:
                corner_radius = (origination[b'topRight'], origination[b'topLeft'], origination[b'bottomLeft'],
                                 origination[b'bottomRight'])
                print(e)
    except Exception as e:
        print(e)

    return corner_radius


def parse_dict_color(_color_):
    try:
        _color_ = eval(str(_color_))
    except Exception as e:
        print(e)
    if b'Clr ' in _color_:
        _color_ = _color_[b'Clr ']
    _color_r = _color_[b'Rd  ']
    _color_g = _color_[b'Grn ']
    _color_b = _color_[b'Bl  ']
    return _color_r, _color_g, _color_b


def rgb_to_hex(rgb):
    """
    将 RGB 颜色值转换为十六进制颜色代码。

    参数:
    rgb (tuple): 一个包含三个整数的元组，分别表示红色、绿色和蓝色分量。

    返回:
    str: 表示十六进制颜色代码的字符串，格式为 "#RRGGBB"。
    """

    if type(rgb) is not tuple:
        rgb = parse_dict_color(rgb)
    # 确保颜色分量在 0 到 255 之间
    r, g, b = [min(255, max(0, int(x))) for x in rgb]
    # 使用 format() 函数将 RGB 颜色值转换为十六进制颜色代码
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


# 定义一个函数来递归地遍历图层树
def traverse_layers(layers, n, soup, geometry=1):
    global workspace, traverse_num, layers_count, manifest_root, element_list, canvas_w, canvas_h
    print("\t")

    if layers.kind == 'psdimage' or layers.name == 'ROOT':
        # print(f"{tn(n)}attr：{dir(layers)}")
        # print('layers._layers:', layers._layers)
        # print('layers._record:', dir(layers._record._get_layer_info()))
        # print('layers._record:', eval(str(layers._record.tobytes())))
        # print('layers._record:', eval(str(layers._record._get_layer_info().tobytes())))
        # print('layers.layer_records:', layers._record._get_layer_info().layer_records)

        # print('layers.channels:', layers.channels)
        # print('layers.color_mode:', layers.color_mode)
        # print('layers.depth:', layers.depth)
        # print('layers.kind:', layers.kind)
        # print('layers.version:', layers.version)

        # try:
        #     layers.count = abs(layers._record._get_layer_info().layer_count)
        # except Exception as e:
        #     layers.count = len(layers)
        # layers_count = layers.count
        layers.outbound = layers.bbox != layers.viewbox
        canvas_w = layers.viewbox[2]
        canvas_h = layers.viewbox[3]

        # print('layers.count:', layers_count)
        print('layers.bbox:', layers.bbox)
        print('layers.viewbox:', layers.viewbox)
        print('layers.outbound:', layers.outbound)
        print('layers.name:', layers.name)
        print('layers.size:', layers.size)

        # Export Preview Image
        layers_pil = layers.topil().convert('RGB')
        layers_pil = crop_image(layers_pil, (layers_pil.width - 1080) // 2, (layers_pil.height - 2412) // 2, 1080, 2412)
        layers_pil = layers_pil.filter(ImageFilter.GaussianBlur(radius=60))
        layers_pil.save(os.path.join(os.path.dirname(workspace), 'bs.jpg'))
        manifest_root = soup.find_all(True)[0].name

        print('\t')
    # sys.exit(8)
    # else:

        # print(layers.clip_layers)
        # print(layers.clipping_layer)

    for layer in layers:

        if layer.visible or 1:

            layer_id = layer.layer_id
            layer_clip = None
            layers_count += not(layer.is_group())

            layer_w = layer.width + layer.width % 2
            layer_h = layer.height + layer.height % 2

            layer_x_left = layer.left
            layer_x_center = (layer.left + layer.right) // 2
            layer_x_right = layer.right

            layer_y_top = layer.top
            layer_y_center = (layer.top + layer.bottom) // 2
            layer_y_bottom = layer.bottom

            layer_x = {
                "left": str(layer_x_left),
                "center": str(layer_x_center),
                "right": str(layer_x_right)
            }
            layer_y = {
                "top": str(layer_y_top),
                "center": str(layer_y_center),
                "bottom": str(layer_y_bottom)
            }

            layer_align_def = 'center'
            layer_alignV_def = 'center'

            # layer.name = layer.name.replace('<', '').replace('>', '')
            layer.file = custom_encrypt(str(layer.layer_id) + str(layer.name))
            layer.suffix = 'png'
            layer.filename = os.path.join(workspace, layer.file + '.' + layer.suffix)
            layer.color = ''

            print(f"{tn(n)}文件名称：{layer.filename}")
            print(f"{tn(n)}图层名称：{layer.name}")
            print(f'{tn(n)}位置：x="{layer_x_center}" y="{layer_y_center}"')
            print(f'{tn(n)}大小：w="{layer_w}" h="{layer_h}"')
            print(f"{tn(n)}不透明度：{layer.opacity}")

            print(f"{tn(n)}图层id：{layer.layer_id}")
            print(f"{tn(n)}上一级: {layer.parent.name}")
            print(f"{tn(n)}效果: {layer.has_effects()}")
            print(f"{tn(n)}可见性: {layer.visible}")
            print(f"{tn(n)}是否为组: {layer.is_group()}")
            print(f"{tn(n)}是否为已剪切: {layer.clipping_layer}")

            if layer.clipping_layer:
                layer_clip = True
            else:
                layer_clip = None
            # print(dir(layer))

            layer.export_mode = 1
            if layer.is_group():
                layer.export_mode = 0

                group_tag_name = 'Group'
                group_tag = soup.new_tag(group_tag_name, attrs={'alias': layer.name, "_layer_id": layer_id})
                if str(layer.parent.name).upper() == 'ROOT':
                    exec(f'soup.{manifest_root}.append(group_tag)')
                else:
                    add_parent_tag(soup, group_tag, layer)

            else:

                # 如果图层是文本图层，则打印文本大小和对齐信息
                if isinstance(layer, psd_tools.api.layers.TypeLayer):
                    layer.export_mode = 0
                    layer.typeface = 0
                    layer.color = ''
                    text_tag_name = 'Text'

                    text_expression = layer._engine_data['EngineDict']['Editor']['Text']
                    text_content = str(text_expression).replace('\\r', '\\n')
                    text_content = eval(str(text_content)).strip()

                    # 纯文本
                    if is_pure_text(text_content):
                        text_format = None
                        text_paras = None
                        # 匹配到 '星期?|周?'
                        if match_weekday(text_content):
                            text_tag_name = 'DateTime'
                            text_format = match_weekday(text_content)
                            text_paras = None
                            text_content = None
                        else:
                            var_name = f'layer_{layer.layer_id}'
                            var_tag = soup.new_tag('Var', attrs={'name': var_name, 'type': 'string', 'expression': f"'{text_content}'"})
                            text_content = f"@{var_name}"
                            exec(f'soup.{manifest_root}.append(var_tag)')
                    else:
                        # 纯数字
                        if text_content.isdigit():
                            var_name = f'layer_{layer.layer_id}'
                            text_format = '%d'
                            text_paras = f'#{var_name}'
                            var_tag = soup.new_tag('Var', attrs={'name': var_name, 'type': 'number', 'expression': f"{text_content}"})
                            text_content = None
                            exec(f'soup.{manifest_root}.append(var_tag)')

                        # 数字 + 文本
                        else:
                            text_format = match_digits(text_content).replace('%d%', '%d%%')
                            text_paras = '#'
                            for p in range(max(text_format.count('%d') - 1, 0)):
                                text_paras += ',#'
                            text_content = None

                    font_family = layer._engine_data['ResourceDict']['FontSet'][0]['Name']
                    font_family = eval(str(font_family).lower())
                    if not layer.typeface:
                        text_font_path = f"etc/{font_family}.ttf"
                        text_type_face = None
                        text_height = None
                    else:
                        text_font_path = None
                        text_type_face = f"{font_family}.ttf"
                        text_height = layer.height

                    # 获取文本图层的对齐方式
                    justification = layer.engine_dict['ParagraphRun']['RunArray'][0]['ParagraphSheet']['Properties']['Justification']
                    justification_str = ['left', 'right', 'center']
                    text_align = justification_str[justification]

                    text_size = layer._engine_data['EngineDict']['StyleRun']['RunArray'][0]['StyleSheet']['StyleSheetData']['FontSize']
                    text_size = min(int(text_size), layer.height)
                    m_text_size = f'-#mTextSize_{text_size}' if not layer.typeface else ''

                    text_color = layer._engine_data['EngineDict']['StyleRun']['RunArray'][0]['StyleSheet']['StyleSheetData']['FillColor']['Values'][1:]
                    text_color_r = text_color[0] * 255
                    text_color_g = text_color[1] * 255
                    text_color_b = text_color[2] * 255
                    text_color = (text_color_r, text_color_g, text_color_b)
                    text_color_ori = rgb_to_hex(tuple(text_color))

                    layer.color = find_overlay_color(layer, text_color_ori)

                    print(f"{tn(n)}文字高度：{layer.height}")
                    print(f"{tn(n)}文字内容：{text_expression}")
                    print(f"{tn(n)}字体名称: {font_family}")
                    print(f"{tn(n)}对齐方式:, {justification}, {text_align}")
                    print(f"{tn(n)}字体大小: {text_size}")
                    print(f"{tn(n)}颜色: {layer.color}")

                    text_attrs = {
                        "x": layer_x[text_align],
                        "y": layer_y[layer_alignV_def] + m_text_size,
                        "align": text_align,
                        "alignV": layer_alignV_def,
                        "color": layer.color,
                        "size": text_size,
                        "textExp": text_content,
                        "format": text_format,
                        "paras": text_paras,
                        "fontPath": text_font_path,
                        "typeface": text_type_face,
                        "alpha": layer.opacity,
                        "alias": layer.name,
                        "h": text_height,
                        "_layer_id": layer_id,
                    }
                    text_tag = soup.new_tag(text_tag_name, attrs={i: text_attrs[i] for i in text_attrs if text_attrs[i] is not None})
                    add_parent_tag(soup, text_tag, layer)
                    # print(soup)

                # 如果图层是形状图层，则打印描边信息
                elif isinstance(layer, psd_tools.api.layers.ShapeLayer) and not layer.has_effects():
                    layer.export_mode = 1
                    debug = 0
                    layer.color = ''
                    # print('Clip:', layer._clip_layers)
                    # print('Clip:', layer._has_clip_target)
                    # print('Clip:', layer.clip_layers)
                    # print('Clip:', layer.has_clip_layers)
                    # print('Clip:', layer._record)
                    # print(dir(layer))

                    if debug:
                        pil_image = layer.topil()
                        # Palette the center point of layer
                        d = max(layer.width // 2, layer.height // 2)
                        if 0 <= d < len(np.array(pil_image)[0]):
                            color_r = np.array(pil_image)[0][d][0]
                            color_g = np.array(pil_image)[0][d][1]
                            color_b = np.array(pil_image)[0][d][2]
                            color_a = layer.opacity
                            color_hex = rgb_to_hex((color_r, color_g, color_b))
                            layer.color = color_hex
                            # print(f"{tn(n)}颜色：RGB({d}, {color_r}, {color_g}, {color_b}, {color_a}), HEX: {layer.color}")

                        if layer.has_origination():
                            origination = layer.origination[0]
                            corner_radius = None
                            rect_tag_name = 'Rectangle'

                            # Rectangle
                            # print(origination.origin_type)
                            if origination.origin_type <= 2:
                                corner_radius = 0
                                text_tag_name = 'Rectangle'

                                if origination.origin_type == 2:
                                    # RoundedRectangle // hasattr(origination, 'radii')
                                    corner_radius = int(parse_corner_radius(origination.radii))

                            else:
                                if layer.clipping_layer or layer.has_effects():
                                    layer.export_mode = 1
                                    layer.visible = False

                                # print(f"{tn(n)}圆角半径: {corner_radius}")

                                rect_attrs = {
                                    "x": layer_x[layer_align_def],
                                    "y": layer_y[layer_alignV_def],
                                    "align": layer_align_def,
                                    "alignV": layer_alignV_def,
                                    "w": layer_w,
                                    "h": layer_h,
                                    "color": layer.color,
                                    "alpha": layer.opacity,
                                    "alias": layer.name,
                                    "cornerRadius": f'{corner_radius},{corner_radius}',
                                    "_layer_id": layer_id,
                                    "_clip_layers": layer_clip,
                                }

                                if layer.has_stroke() and layer.export_mode == 0:
                                    # print(layer.stroke.content)
                                    if b'Grad' not in layer.stroke.content:
                                        rect_attrs['strokeColor'] = rgb_to_hex(layer.stroke.content)
                                        rect_attrs['strokeAlign'] = 'inner'
                                        rect_attrs['weight'] = layer.stroke.line_width * layer.stroke.enabled
                                        rect_attrs['cap'] = layer.stroke.line_cap_type
                                    else:
                                        layer.export_mode = 1
                                    # print(f"{tn(n)}描边信息：{layer.stroke}, width: {layer.stroke.line_width * layer.stroke.enabled}, color: {layer.stroke.color}, alpha: {layer.stroke.opacity}, align: {layer.stroke.line_alignment}, cap: {layer.stroke.line_cap_type}")

                                if layer.export_mode == 0:
                                    rect_tag = soup.new_tag(rect_tag_name, attrs={i: rect_attrs[i] for i in rect_attrs if rect_attrs[i] is not None})
                                    add_parent_tag(soup, rect_tag, layer)
                            # print(soup)

                # 如果图层是填充图层，则导出为图片
                elif isinstance(layer, psd_tools.api.layers.FillLayer):
                    print(f"{tn(n)}颜色: {rgb_to_hex(layer._data)}")
                    layer.export_mode = 1

            if layer.export_mode:

                image_x = int(layer_x[layer_align_def])
                image_y = int(layer_y[layer_alignV_def])

                layer.empty = layer.width == layer.height == 0
                if layer.is_group() or layer.empty:
                    pass

                else:
                    if layer.has_effects():
                        image = layer.composite()
                    else:
                        image = layer.topil()
                    # print(image)
                    # image = image.resize((layer_w, layer_h), Image.Resampling.LANCZOS)

                    # elif layer.width > canvas_w and layer.height < canvas_h:
                    #     image_x = canvas_w // 2
                    #     layer_h = layer_h
                    #     image = crop_image(image, abs(layer_x_left), 0, min(layer_w, canvas_w), layer_h)
                    # elif layer.width < canvas_w and layer.height > canvas_h:
                    #     image_y = canvas_h // 2
                    #     layer_w = layer_w
                    #     layer_h = min(layer_h, canvas_h)
                    #     image = crop_image(image, 0, abs(layer_y_top), layer_w, min(layer_h, canvas_h))
                    # else:
                    #     image = image

                    if (layer.width > canvas_w or layer.height > canvas_h) and has_transparency(image):
                        try:
                            layer_r = layer.composite()
                        except Exception as e:
                            layer_r = layer.topil()
                        layer_r_bbox = layer_r.getbbox()
                        image = layer_r.crop(layer_r_bbox)

                        if layer.width > canvas_w or layer.height > canvas_h:
                            # print(layer_r_bbox)

                            image_x = int(layer_x[layer_align_def]) - layer.width // 2 - min(abs(layer_x_left), 0) + layer_r_bbox[0] + (layer_r_bbox[2] - layer_r_bbox[0]) // 2
                            image_y = int(layer_y[layer_alignV_def]) - layer.height // 2 - min(abs(layer_y_top), 0) + layer_r_bbox[1] + (layer_r_bbox[3] - layer_r_bbox[1]) // 2

                            # 对齐方式默认为 center
                            layer_w = image.width + (image.width % 2)
                            layer_h = image.height + (image.height % 2)

                        if image.width > canvas_w and image.height > canvas_h:
                            image_x = canvas_w // 2
                            image_y = canvas_h // 2
                            layer_w = canvas_w
                            layer_h = canvas_h
                            image = crop_image(image, abs(layer_x_left), abs(layer_y_top), layer_w, layer_h)

                    if image.width >= canvas_w and image.height >= canvas_h and has_transparency(image) is False:
                        image = image.convert('RGB')
                        layer.suffix = 'jpg'
                        layer.filename = os.path.join(workspace, layer.file + '.' + layer.suffix)
                    image.save(layer.filename)

                    # Call pngquant with desired options
                    image_compress_mode = 1
                    if layer.suffix == 'png' and image_compress_mode:
                        image_compress = subprocess.call(["./pngquant", "-v", "-f", "--ext", ".png", f"{layer.filename}"])
                        #  "--quality", "70-80", "--speed", "5"
                        print(image_compress)
                    # sys.exit(8)

                image_tag_name = 'Image'

                image_attrs = {
                    "x": image_x,
                    "y": image_y,
                    "align": layer_align_def,
                    "alignV": layer_alignV_def,
                    "src": f'{os.path.basename(workspace)}/{layer.file}.{layer.suffix}',
                    "w": layer_w,
                    "h": layer_h,
                    "pivotX": f'{layer_w}/2',
                    "pivotY": f'{layer_h}/2',
                    "rotation": 0,
                    "alias": layer.name,
                    "visibility": int(1 - layer.clipping_layer) if layer.clipping_layer else None,
                    "layer_id": layer_id,
                    "clip_layers": layer_clip,
                    "has_effects": layer.has_effects() if layer.has_effects() else None,
                    "layer_effects": layer.effects if layer.has_effects() else None,
                }

                image_tag = soup.new_tag(image_tag_name, attrs={i: image_attrs[i] for i in image_attrs if image_attrs[i] is not None})
                add_parent_tag(soup, image_tag, layer)

            print('\n')

            # 如果图层是组合图层，则递归遍历其子图层
            if layer.is_group():
                n += 1
                traverse_num += 1
                traverse_layers(layer, n, soup)

            # if layer.clip_layers:
            # layer.composite()
            # if layer.color:
            #     pixels = image.load()
            #     width, height = image.size
            #     if layer.color:
            #         for x in range(width):
            #             for y in range(height):
            #                 r, g, b, a = pixels[x, y]
            #                 if a > 0:
            #                     pixels[x, y] = tuple(int(layer.color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)) + (
            #                         a,)

    return soup


def check(directory, target_num):
    # 列出目录中的所有文件和子目录
    files = os.listdir(directory)

    # 过滤出目录中的文件
    files = [file for file in files if os.path.isfile(os.path.join(directory, file))]

    # 返回文件数量
    return len(files) >= target_num + 1


def main(file_path, folder_name='assets'):
    global workspace, traverse_num, layers_count, psd
    _folder = os.path.dirname(file_path)
    _file = os.path.splitext(os.path.basename(file_path))[0]

    workspace = os.path.join(_folder, _file, folder_name)
    if not os.path.exists(workspace):
        os.makedirs(workspace)
    maml_xml = os.path.join(_folder, _file, 'maml.xml')

    # 加载 PSD 文件
    if file_path.endswith('.psd'):
        psd = PSDImage.open(file_path)

        # 遍历次数
        traverse_num = 0

        # 图层总数量
        layers_count = 0

        # 创建 Soup 对象
        soup = BeautifulSoup(maml_sample_xml, 'lxml-xml')

        # 遍历图层开始
        soup = traverse_layers(psd, 0, soup)

        traverse_dict = {'traverse_num': traverse_num, 'layers_count': layers_count}

        # 打印结果
        print(traverse_dict)

        # 验证图片数量
        verify = check(workspace, layers_count)
        if verify:
            print(f'{GREEN}mFiles Number Verify: {verify}')

        with open(maml_xml, 'w', encoding='utf-8') as fb:
            fb.write(str(soup.prettify()).replace('="-', '="0-'))
        # import tools.order
        # tools.order.orderXML(maml_xml, None, 0)

    else:
        print(f"Error: File must be '*.psd'")


if __name__ == '__main__':

    # PSD 文件路径
    # psd_path = '/Users/wangshilong/Desktop/导出/待办/CYKON/R/3 虫茧/OPPO/PSD/4x2_1_大复合组件.psd'
    # psd_path = '/Users/wangshilong/Desktop/1x/jsx/GetterXml/Arc+Rect.psd'
    # psd_path = '/Users/wangshilong/Desktop/导出/待办/CYKON/RM/5 奶油风轻拟态/奶油风轻拟态/源文件/psd/电量.psd'
    # psd_path = '/Users/wangshilong/Desktop/导出/待办/CYKON/RM/5 奶油风轻拟态/奶油风轻拟态/源文件/psd/步数.psd'
    # psd_path = '/Users/wangshilong/Desktop/导出/待办/CYKON/RM/5 奶油风轻拟态/奶油风轻拟态/源文件/psd/复合组件.psd'
    # psd_path = '/Users/wangshilong/Desktop/导出/待办/CYKON/RM/5 奶油风轻拟态/奶油风轻拟态/源文件/psd/object.psd'
    # psd_path = '/Users/wangshilong/Desktop/导出/待办/麦禾-木兰/250.和米奇一起来玩耍 锁屏切图_3564116295/和米奇一起来玩耍1-3.psd'
    # psd_path = '/Users/wangshilong/Desktop/导出/待办/麦禾-木兰/246.趣味唐老鸭 锁屏切图/趣味唐老鸭 锁屏切图1-4-C.psd'
    # psd_path = '/Users/wangshilong/Desktop/导出/待办/麦禾-木兰/247.维尼的小确幸_364657375/维尼熊的故事书锁屏-C.psd'
    psd_path = '/Users/wangshilong/Desktop/导出/待办/麦禾-木兰/278.帮维尼找蜜罐主题锁屏切图_920326985/PSD/闯关动态开发-C2.psd'
    print('请把所有内容放在一个组内')
    main(psd_path)
