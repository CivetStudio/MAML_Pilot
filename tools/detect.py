# import os
#
# def detectButtonAlign(process_xml):
#
#     with open(process_xml, 'r', encoding='utf-8') as f:
#         lines = f.readlines()
#
#     # 找出包含【name=""】
#     for i, line in enumerate(lines, 1):
#         if '<Button' in line and ('align=' in line or 'alignV=' in line):
#             print(line.strip())  # 输出符合条件的整行内容
#             print("Line:", i)  # 输出行号
#             print("\t")
#
#
# # 示例用法
# maml_main_xml = '/Users/wangshilong/Downloads/3D暴富兔 10主题包/国内版/OPPO/lockscreen/advance/maml.xml'
# detectButtonAlign(maml_main_xml)

import os
import sys
import pyperclip
from lxml import etree as lxml

maml_main_xml = pyperclip.paste().replace('\\', '/').replace('"', '')

maml_rule_file = "maml.xml"
maml_file_name = os.path.basename(maml_main_xml)

# 判断 maml_file_name 是否以 maml_rule_file 结尾
if maml_rule_file not in maml_file_name:
    print(f"Error: File must be '{maml_rule_file}'")
    sys.exit(1)

print('\t')
print(f'Source: {maml_main_xml}\n')


def get_line_number(file_path, target_str):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            if target_str in line:
                return i
    return None


def detect_button_align(process_xml):
    # parser = lxml.XMLParser(recover=True)
    tree = lxml.parse(process_xml)
    # tree = lxml.parse(process_xml, parser)
    root = tree.getroot()

    # for tag in root.xpath('//Var'):
    # for tag in root.xpath('//Button[@align or @alignV]'):
    for tag in root.xpath('//Image[@name]'):
        # print(tag)
        name = tag.get('name')
        print(f'<Command target="{name}.animation" value="stop" />')
        print(f'<Command target="{name}.animation" value="play" />')
        # 获取元素在 XML 文档中的行号
        line_number = tag.sourceline

        if line_number is not None:
            # 输出行号和整行内容
            # print("Line:", line_number)
            with open(process_xml, encoding="utf-8") as f:
                lines = f.readlines()
                line_content = lines[line_number - 1].strip()
                print(line_content, '\n')


# 示例用法
detect_button_align(maml_main_xml)
