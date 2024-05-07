<<<<<<< Updated upstream
import os
import sys
import re
import time

import pyperclip
import shutil
from lxml import etree as lxml

import dev.Refactor.refactor


def convert_to_source(input_file, output_file, order_mode=1):

    tree = lxml.parse(input_file)
    root = tree.getroot()

    # 使用XPath查找元素
    key_expression = root.xpath("//Var[@name='Key']")

    # 如果找到匹配的元素，则打印其文本内容
    if key_expression:
        key_exp = key_expression[0].get('expression')
        var_dict = eval(dev.Refactor.refactor.aes_decode(eval(key_exp)))
        print("Found Key expression:", key_expression[0].get('expression'))
        print(var_dict)
    else:
        # 如果找不到匹配的元素，则引发异常
        raise Exception("Key expression not found in XML")

    shutil.copy(input_file, output_file)
    for key, value in var_dict.items():
        replace_string_in_xml(output_file, key, value)

    # order_mode 导致注释丢失，但可以格式化
    if order_mode:
        import tools.order
        tools.order.orderXML(output_file)

    print('Done, anti-xml() Success!')


def replace_string_in_xml(xml_file, old_str, new_str):

    with open(xml_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(xml_file, 'w', encoding='utf-8') as file:
        for line in lines:
            if old_str in line:
                line = line.replace(old_str, new_str)
            file.write(line)


if __name__ == '__main__':
    maml_main_xml = pyperclip.paste().replace('\\', '/').replace('"', '')

    maml_file_name = os.path.basename(maml_main_xml)
    maml_rule_file = 'manifest.xml'
    _origin_xml = maml_main_xml.replace(maml_rule_file, "source.xml")

    # 判断 maml_file_name 是否以 maml_rule_file 结尾
    if maml_rule_file not in maml_file_name:
        print(f"Error: File must be '{maml_rule_file}'")
        sys.exit(1)

    print('\t')
    print(f'Source: {maml_main_xml}\n')

    # 示例用法
    input_xml_file = maml_main_xml
    output_xml_file = _origin_xml
    convert_to_source(input_xml_file, output_xml_file, 0)
=======
import os
import sys
import re
import time

import pyperclip
import shutil
from lxml import etree as lxml

import dev.Refactor.refactor


def convert_to_source(input_file, output_file, order_mode=1):

    tree = lxml.parse(input_file)
    root = tree.getroot()

    # 使用XPath查找元素
    key_expression = root.xpath("//Var[@name='Key']")

    # 如果找到匹配的元素，则打印其文本内容
    if key_expression:
        key_exp = key_expression[0].get('expression')
        var_dict = eval(dev.Refactor.refactor.aes_decode(eval(key_exp)))
        print("Found Key expression:", key_expression[0].get('expression'))
        print(var_dict)
    else:
        # 如果找不到匹配的元素，则引发异常
        raise Exception("Key expression not found in XML")

    shutil.copy(input_file, output_file)
    for key, value in var_dict.items():
        replace_string_in_xml(output_file, key, value)

    # order_mode 导致注释丢失，但可以格式化
    if order_mode:
        import tools.order
        tools.order.orderXML(output_file)

    print('Done, anti-xml() Success!')


def replace_string_in_xml(xml_file, old_str, new_str):

    with open(xml_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(xml_file, 'w', encoding='utf-8') as file:
        for line in lines:
            if old_str in line:
                line = line.replace(old_str, new_str)
            file.write(line)


if __name__ == '__main__':
    maml_main_xml = pyperclip.paste().replace('\\', '/').replace('"', '')

    maml_file_name = os.path.basename(maml_main_xml)
    maml_rule_file = 'manifest.xml'
    _origin_xml = maml_main_xml.replace(maml_rule_file, "source.xml")

    # 判断 maml_file_name 是否以 maml_rule_file 结尾
    if maml_rule_file not in maml_file_name:
        print(f"Error: File must be '{maml_rule_file}'")
        sys.exit(1)

    print('\t')
    print(f'Source: {maml_main_xml}\n')

    # 示例用法
    input_xml_file = maml_main_xml
    output_xml_file = _origin_xml
    convert_to_source(input_xml_file, output_xml_file, 0)
>>>>>>> Stashed changes
