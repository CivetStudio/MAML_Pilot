import os
import sys
import pyperclip
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape, unescape

maml_main_xml = pyperclip.paste().replace('\\', '/').replace('"', '')

maml_file_name = os.path.basename(maml_main_xml)
maml_rule_file = '.xml'

# 判断 maml_file_name 是否以 maml_rule_file 结尾
if maml_rule_file not in maml_file_name:
    print(f"Error: File must be '{maml_rule_file}'")
    sys.exit(1)

print('\t')
print(f'Source: {maml_main_xml}\n')


def convert_to_unicode(input_file, output_file):
    # 解析 XML 文件
    tree = ET.parse(input_file)
    root = tree.getroot()

    # 递归函数，将中文字符转换为 Unicode 编码表示
    def convert_element(element):
        if element.text is not None:
            element.text = ''.join(f'&#{ord(char)};' if ord(char) > 127 else escape(char) for char in element.text)
        for key, value in element.attrib.items():
            element.attrib[key] = ''.join(f'&#{ord(char)};' if ord(char) > 127 else escape(char) for char in value)
        for child in element:
            convert_element(child)

    # 将中文字符转换为 Unicode 编码表示
    convert_element(root)

    # 将 XML 树转换为字符串，并替换特殊字符
    xml_str = ET.tostring(root, method='xml', encoding='unicode')
    xml_str = xml_str.replace('&amp;', '&').\
        replace('<Lockscreen', '<?xml version="1.0" encoding="utf-8"?><Lockscreen').replace('vibrate="false">', 'vibrate="false"><!-- 欢迎定制锁屏：灵貓 QQ 1876461209 --><!-- 违规抄袭将依据《中华人民共和国民法通则》《中华人民共和国著作权法》《计算机软件保护条例》《软件产品管理办法》《侵权责任法》《中华人民共和国知识产权法》追究法律责任 -->')

    # 保存修改后的 XML 到输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)


# 反向函数，将 Unicode 编码转换为中文字符
def convert_to_chinese(input_file, output_file):
    # 解析 XML 文件
    tree = ET.parse(input_file)
    root = tree.getroot()

    # 将 XML 树转换为字符串，并替换特殊字符
    xml_str = ET.tostring(root, method='xml', encoding='unicode')
    xml_str = xml_str.replace('&', '&amp;').\
        replace('<Lockscreen', '<?xml version="1.0" encoding="utf-8"?><Lockscreen').replace('vibrate="false">', 'vibrate="false"><!-- 欢迎定制锁屏：灵貓 QQ 1876461209 --><!-- 违规抄袭将依据《中华人民共和国民法通则》《中华人民共和国著作权法》《计算机软件保护条例》《软件产品管理办法》《侵权责任法》《中华人民共和国知识产权法》追究法律责任 -->')

    # 将 Unicode 编码表示转换为中文字符
    xml_str = unescape(xml_str)

    # 保存转换后的 XML 到输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)


# 示例用法
input_xml_file = maml_main_xml
output_xml_file = maml_main_xml.replace('.xml', '_new.xml')
convert_to_unicode(input_xml_file, output_xml_file)
# convert_to_chinese(input_xml_file, output_xml_file)
