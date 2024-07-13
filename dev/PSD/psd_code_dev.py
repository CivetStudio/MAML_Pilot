import math
import sys

from PIL import Image
import pyperclip
from psd_tools import PSDImage
import psd_tools
from psd_tools.constants import ChannelID
from psd_tools.api.shape import RoundedRectangle
from psd_tools.api.adjustments import SolidColorFill
import uuid
# from psd_tools.psd.descriptor import Descriptor

import numpy as np
import re


def tn(n):
    # 如果你想输出 \t\t\t，你可以直接写成 f"\\t\\t\\t"，不需要变量 n
    _num_ = 0
    result = ''
    while _num_ <= n:
        result = result + '\t'
        _num_ += 1
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
def traverse_layers(layers, n=0):
    global num
    print("\t")

    if layers.name == 'ROOT':
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

        print('layers.count:', layers._record._get_layer_info().layer_count)
        print('layers.count:', len(layers))
        print('layers.bbox:', layers.bbox)
        print('layers.viewbox:', layers.viewbox)
        print('layers.name:', layers.name)
        print('layers.size:', layers.size)
        print(uuid.uuid5())

        layers_pil = layers.topil().save('preview.png')
        # layers_pil.show()
        print('\t')
    # sys.exit(8)

    for layer in layers:

        if layer.visible or 1:

            # 获取图像文件中的标记块
            # metadata = layer.tagged_blocks
            # print(metadata)
            # 打印元数据
            # print(dir(metadata.get_data(b'TySh')))
            # print(metadata.get_data(b'TySh'))
            # print(metadata.get_data(b'lclr'))

            layer_w = layer.width + layer.width % 2
            layer_h = layer.height + layer.height % 2

            layer_x_left = layer.left
            layer_x_center = (layer.left + layer.right) // 2
            layer_x_right = layer.right

            layer_y_top = layer.top
            layer_y_center = (layer.top + layer.bottom) // 2
            layer_y_bottom = layer.bottom

            layer_align_def = 'center'
            layer_alignV_def = 'center'

            layer_x = eval(f'layer_x_{layer_align_def}') + eval(f'layer_x_{layer_align_def}') % 2
            layer_y = eval(f'layer_y_{layer_align_def}') + eval(f'layer_y_{layer_align_def}') % 2

            # 切图
            if layer.topil() is not None:
                layer.topil().save(f'topil.png')
            # layer.topil().save(f'topil_{layer.layer_id}.png')

            print(f"{tn(n)}图层名称：{layer.name}")
            print(f'{tn(n)}位置：x="{layer_x}" y="{layer_y}"')
            print(f'{tn(n)}大小：w="{layer_w}" h="{layer_h}"')
            print(f"{tn(n)}不透明度：{layer.opacity}")

            print(f"{tn(n)}图层id：{layer.layer_id}")
            print(f"{tn(n)}上一级: {layer.parent.name}")
            print(f"{tn(n)}效果: {layer.has_effects()}")
            print(f"{tn(n)}可见性: {layer.visible}")
            print(f"{tn(n)}是否为组: {layer.is_group()}")

            # 如果图层是文本图层，则打印文本大小和对齐信息
            if isinstance(layer, psd_tools.api.layers.TypeLayer):
                # print(dir(layer))

                text_content = layer._engine_data['EngineDict']['Editor']['Text']
                text_content = str(text_content).replace('\\r', '\\n')
                text_content = bytes(text_content, encoding='utf-8')
                font_family = layer._engine_data['ResourceDict']['FontSet'][0]['Name']

                print(f"{tn(n)}文字高度：{layer.height}")
                print(f"{tn(n)}文字内容：{text_content}")
                print(f"{tn(n)}文字内容：'''{eval(text_content)}'''")
                print(f"{tn(n)}字体名称: {eval(str(font_family))}")

                # 获取文本图层的对齐方式
                justification = layer.engine_dict['ParagraphRun']['RunArray'][0]['ParagraphSheet']['Properties']['Justification']
                justification_str = ['left', 'right', 'center']
                print(f"{tn(n)}对齐方式:, {justification}, {justification_str[justification]}")

                text_size = layer._engine_data['EngineDict']['StyleRun']['RunArray'][0]['StyleSheet']['StyleSheetData']['FontSize']
                print(f"{tn(n)}字体大小: {text_size}")

                text_color = layer._engine_data['EngineDict']['StyleRun']['RunArray'][0]['StyleSheet']['StyleSheetData']['FillColor']['Values'][1:]
                text_color_r = text_color[0] * 255
                text_color_g = text_color[1] * 255
                text_color_b = text_color[2] * 255
                text_color = (text_color_r, text_color_g, text_color_b)
                text_color = rgb_to_hex(tuple(text_color))
                print(f"{tn(n)}颜色: {text_color}")

                # 字体还有其他信息Json
                # print('?', layer._engine_data)
                # pyperclip.copy(str(layer._engine_data))

                # print(f"{tn(n)}{layer.kind == 'type'}")

                # sys.exit(10)
                # print("\n")

            # 如果图层是形状图层，则打印描边信息
            if isinstance(layer, psd_tools.api.layers.ShapeLayer):
                # print(dir(layer))
                if layer.has_origination():
                    origination = layer.origination[0]
                    if hasattr(origination, 'radii'):
                        corner_radius = parse_corner_radius(origination.radii)
                        print(f"{tn(n)}圆角半径: {corner_radius}")
                    else:
                        corner_radius = None
                    # print(f"{tn(n)}类型: {type(origination).__name__}, bbox: {origination.bbox}, radii: {corner_radius}")

                    # print('origination._data:', origination._data)

                    #     print('shape.bbox:', shape.bbox)
                    #     print('shape.index:', shape.index)
                    #     print('shape.invalidated:', shape.invalidated)
                    #     print('shape.origin_type:', shape.origin_type)
                    #     print('shape.radii:', shape.radii)
                    #     print('shape.resolution:', shape.resolution)

                if layer.has_stroke():

                    # print(type(layer.stroke.content))
                    layer.stroke.color = rgb_to_hex(layer.stroke.content)
                    print(
                        f"{tn(n)}描边信息：{layer.stroke}, width: {layer.stroke.line_width * layer.stroke.enabled}, color: {layer.stroke.color}, alpha: {layer.stroke.opacity}, align: {layer.stroke.line_alignment}, cap: {layer.stroke.line_cap_type}")

                    # print('enabled:', layer.stroke.enabled)
                    # print('fill_enabled:', layer.stroke.fill_enabled)
                    # print('line_width:', layer.stroke.line_width)
                    # print('line_dash_set:', layer.stroke.line_dash_set)
                    # print('line_dash_offset:', layer.stroke.line_dash_offset)
                    # print('line_cap_type:', layer.stroke.line_cap_type)
                    # print('miter_limit:', layer.stroke.miter_limit)
                    # print('line_join_type:', layer.stroke.line_join_type)
                    # print('line_alignment:', layer.stroke.line_alignment)
                    # print('scale_lock:', layer.stroke.scale_lock)
                    # print('stroke_adjust:', layer.stroke.stroke_adjust)
                    # print('opacity:', layer.stroke.opacity)
                    # print('content:', layer.stroke.content)
                    # print('__repr__:', layer.stroke.__repr__)

                    # print("\n")
                # sys.exit(10)

                # print(f"{tn(n)}{layer.kind == 'shape'}")

            if isinstance(layer, psd_tools.api.layers.FillLayer):
                print(f"{tn(n)}颜色: {rgb_to_hex(layer._data)}")

            # 如果图层有颜色，则打印颜色信息
            if isinstance(layer, psd_tools.api.layers.ShapeLayer):
                # print(dir(layer.topil()))
                pil_image = layer.topil()

                if layer.has_effects():
                    try:
                        for color in range(len(layer.effects)):
                            if str(layer.effects[color]) == 'ColorOverlay':
                                effects_color = rgb_to_hex(str(layer.effects[color].color))
                                effects_opacity = layer.effects[color].opacity
                                print(f"{tn(n)}颜色叠加: {effects_color}, {effects_opacity}%")
                    except Exception as e:
                        print(e)
                    # print(layer.effects[0].opacity)
                    # print(layer.effects[0].present)
                    # print(layer.effects[0].shown)
                    # print(layer.effects[0].value)
                    # print(layer.effects[0].blend_mode)

                # Method #1
                # image_colors = pil_image.getcolors()
                # colors = []
                # if image_colors:
                #     colors.extend([color[1] for color in image_colors])
                #     print(colors[len(colors) // 2 -1])

                # Method #2
                # Palette the center point of layer
                d = max(layer.width // 2, layer.height // 2)
                if 0 <= d < len(np.array(pil_image)[0]):
                    color_r = np.array(pil_image)[0][d][0]
                    color_g = np.array(pil_image)[0][d][1]
                    color_b = np.array(pil_image)[0][d][2]
                    color_a = layer.opacity
                    color_hex = rgb_to_hex((color_r, color_g, color_b))
                    print(f"{tn(n)}颜色：RGB({d}, {color_r}, {color_g}, {color_b}, {color_a}), HEX: {color_hex}")

            print('\n')

            # 如果图层是组合图层，则递归遍历其子图层
            if layer.is_group():
                num = num + 1
                traverse_layers(layer, num)


# PSD 文件路径
psd_path = '/Users/wangshilong/Desktop/导出/待办/CYKON/R/3 虫茧/OPPO/PSD/4x2_1_大复合组件.psd'
psd_path = '/Users/wangshilong/Desktop/1x/jsx/GetterXml/Arc+Rect.psd'
# psd_path = '/Users/wangshilong/Desktop/导出/待办/CYKON/RM/4 落日余晖/小米/源文件/分割PSD/160.psd'

# 加载 PSD 文件
psd = PSDImage.open(psd_path)

# 调用函数来遍历所有图层并输出信息
num = 0
traverse_layers(psd)


# def traverse_layers(layers, n=0):
#     global num
#     print("\t")
#
#     # for layer in layers:
#     #     for i in range(len(dir(layer))):
#     #         name = dir(psd)[i]
#     #         # print(name)
#     #         if name.startswith('__') and not name.isdigit():
#     #             pass
#     #         else:
#     #             # print(f'psd.{name}', eval(f'psd.{name}'))
#     #             psd_obj_name = f'psd.{name}'
#     #             psd_obj = eval(f'psd.{name}')
#     #             print(psd_obj_name, psd_obj)
#     #             for j in range(len(dir(psd_obj))):
#     #                 name_j = dir(psd_obj)[j]
#     #                 if name_j.startswith('__'):
#     #                     pass
#     #                 else:
#     #                     j_psd_obj_name = f'{psd_obj_name}.{name_j}'
#     #                     j_psd_obj = f'{psd_obj_name}.{name_j}'
#     #                     print('\t', psd_obj_name, psd_obj)
#     #
#     # sys.exit(10)
