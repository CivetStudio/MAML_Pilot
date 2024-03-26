import os
import sys
import re
import pyperclip
from bs4 import BeautifulSoup
import shutil


orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


BeautifulSoup.prettify = prettify


def convert_to_source(key_file, input_file, output_file, order_mode=1, soup_replace=0):

    var_dict = {}
    soup = BeautifulSoup(open(key_file), 'lxml-xml')
    for var in reversed(soup.find_all('Aliasing')):
        var_after = var.get('after')
        var_init = var.get('initial')
        var_dict[var_after] = var_init
        if __name__ == '__main__':
            print(f"{{'{var_after}': '{var_init}'}}")
    soup.clear()

    if not soup_replace:
        shutil.copy(input_file, output_file)
        for key, value in var_dict.items():
            replace_string_in_xml(output_file, key, value)

    else:
        soup = BeautifulSoup(open(input_file), 'lxml-xml')
        soup_content = str(soup)
        for key, value in var_dict.items():
            soup_content = str(soup_content).replace(key, value)
        soup = BeautifulSoup(soup_content, 'lxml-xml')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify(indent_width=4).replace('    ', '\t')))

    # order_mode 导致注释丢失，但可以格式化
    if order_mode:
        import tools.order
        tools.order.orderXML(output_file)

    print('Done, anti-xml() Success!')


def replace_string_in_xml(xml_file, old_str, new_str):

    with open(xml_file, 'r') as file:
        lines = file.readlines()

    with open(xml_file, 'w') as file:
        for line in lines:
            if old_str in line:
                line = line.replace(old_str, new_str)
            file.write(line)


if __name__ == '__main__':
    maml_main_xml = pyperclip.paste().replace('\\', '/').replace('"', '')

    maml_file_name = os.path.basename(maml_main_xml)
    maml_rule_file = 'manifest.xml'
    _origin_xml = maml_main_xml.replace(maml_rule_file, "source.xml")
    _anti_xml = maml_main_xml.replace(maml_rule_file, "anti.xml")

    # 判断 maml_file_name 是否以 maml_rule_file 结尾
    if maml_rule_file not in maml_file_name:
        print(f"Error: File must be '{maml_rule_file}'")
        sys.exit(1)

    print('\t')
    print(f'Source: {maml_main_xml}\n')

    # 示例用法
    key_xml_file = _anti_xml
    input_xml_file = maml_main_xml
    output_xml_file = _origin_xml
    convert_to_source(key_xml_file, input_xml_file, output_xml_file, 1, 0)
