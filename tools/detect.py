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
    # for tag in root.xpath('//Image[@name]'):
    #     # print(tag)
    #     name = tag.get('name')
    #     print(f'<Command target="{name}.animation" value="stop" />')
    #     print(f'<Command target="{name}.animation" value="play" />')
    #     # 获取元素在 XML 文档中的行号
    #     line_number = tag.sourceline
    #
    #     if line_number is not None:
    #         # 输出行号和整行内容
    #         # print("Line:", line_number)
    #         with open(process_xml, encoding="utf-8") as f:
    #             lines = f.readlines()
    #             line_content = lines[line_number - 1].strip()
    #             print(line_content)
    #         print('\n')

    detect_var = 0
    if detect_var:
        for tag in root.xpath('//Var'):
            if tag.get('expression') and tag.get('expression').isnumeric() or tag.get('const') or tag.get('persist'):

                print(tag.get('name'), tag.get('expression'))
                # 获取元素在 XML 文档中的行号
                line_number = tag.sourceline

                if line_number is not None:
                    # 输出行号和整行内容
                    print("Line:", line_number)
                    with open(process_xml, encoding="utf-8") as f:
                        lines = f.readlines()
                        line_content = lines[line_number - 1].strip()
                        print(line_content)
                    print('\n')

    from dev.var_name import custom_encrypt, custom_decrypt
    var_origin_collection = []
    var_encode_collection = []
    for tag in root.xpath('//Var[@name]'):
        parent_tag_name = tag.getparent().tag
        if parent_tag_name != 'Weather':
            var_name = str(tag.get('name'))
            var_origin_collection.append(var_name)
            var_name_encode = custom_encrypt(var_name)
            var_name_decode = custom_decrypt(var_name_encode)
            # if bool(var_name == var_name_decode) is False:
            # print(f"{var_name}: {var_name_encode}, {var_name_decode} \n")
    var_origin_collection.sort(key=len, reverse=True)
    for i in range(len(var_origin_collection)):
        var_encode_collection.append(custom_encrypt(var_origin_collection[i]))
    print(var_origin_collection)
    print(var_encode_collection)

    detect_image = 0
    if detect_image:
        for tag in root.xpath('//Image'):
            if tag.get('srcid') and ('/' in tag.get('srcid') or '%' in tag.get('srcid')):

                print(tag.get('src'), tag.get('srcid'))
                # 获取元素在 XML 文档中的行号
                line_number = tag.sourceline

                if line_number is not None:
                    # 输出行号和整行内容
                    print("Line:", line_number)
                    with open(process_xml, encoding="utf-8") as f:
                        lines = f.readlines()
                        line_content = lines[line_number - 1].strip()
                        print(line_content)
                    print('\n')


detect_button_align(maml_main_xml)
