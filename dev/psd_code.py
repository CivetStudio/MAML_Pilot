from psd_tools import PSDImage
import psd_tools
from psd_tools.constants import ChannelID
import numpy as np


# 定义一个函数来递归地遍历图层树
def traverse_layers(layers):
    print("\t")
    for layer in layers:
        # 打印图层的名称
        print(f"图层名称：{layer.name}")

        # 打印图层的位置和大小信息
        print(f"位置：({layer.left}, {layer.top}), 大小：{layer.width}x{layer.height}")

        # 打印图层的不透明度
        print(f"不透明度：{layer.opacity}")

        # 如果图层是文本图层，则打印文本大小和对齐信息
        if isinstance(layer, psd_tools.api.layers.TypeLayer):
            print(f"文字高度：{layer.height}")
            print(f"文字内容：{layer.text}")
            print("\n")

        # 如果图层是形状图层，则打印描边信息
        if isinstance(layer, psd_tools.api.layers.ShapeLayer):
            if layer.has_stroke():
                stroke_info = layer.stroke
                print(f"描边信息：{stroke_info}")
                print("\n")

        # 如果图层有颜色，则打印颜色信息
        if isinstance(layer, psd_tools.api.layers.ShapeLayer):
            pil_image = layer.topil()
            d = max(layer.width // 2, layer.height // 2)
            color_r = np.array(pil_image)[0][d][0]
            color_g = np.array(pil_image)[0][d][1]
            color_b = np.array(pil_image)[0][d][2]
            color_a = np.array(pil_image)[0][d][3]
            print(f"颜色：RGB({d}, {color_r}, {color_g}, {color_b}, {color_a})")
            if layer.has_origination():
                origination = layer.origination
                print(f"类型：{origination}")
            print("\n")

        # 如果图层是组合图层，则递归遍历其子图层
        if layer.is_group():
            traverse_layers(layer)
            print("\n")

# PSD 文件路径
psd_path = '/Users/wangshilong/Desktop/导出/待办/CYKON/R/3 虫茧/OPPO/PSD/4x2_1_大复合组件.psd'
psd_path = '/Users/wangshilong/Desktop/1x/jsx/GetterXml/Arc+Rect.psd'

# 加载 PSD 文件
psd = PSDImage.open(psd_path)

# 调用函数来遍历所有图层并输出信息
traverse_layers(psd)
