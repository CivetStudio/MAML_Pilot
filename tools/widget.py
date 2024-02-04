"""
华为万象小组件代码转小米小部件
(使用库：pyperclip、bs4)
0.pyperclip传入路径，读取所有 maml.xml 文件，并对文件进行以下操作：
1.将根标签 Lockscreen 改为 Widget，将 version 属性的值改为 2，将  frameRate 属性的值改为 0，将 screenWidth 属性的值改为 1080，将 screenHeight 属性去除，将 displayDesktop 属性去除
2.删除 time="1876461209000" 所属的 AniFrame 标签
3.替换 disabled="miui" 为空字符
4.替换 _miui_ 为空字符
5.删除带有 _harmony_ 属性的 ExternalCommands 标签
6.将 i_Hidden 标签的内容放置在最外面
7.保存并替换原来的maml.xml
"""

import os
import re
import pyperclip
from bs4 import BeautifulSoup
import order


orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


BeautifulSoup.prettify = prettify


def process_maml_xml(xml_content, file_path):
    # 使用BeautifulSoup解析XML内容，使用lxml-xml解析器
    soup = BeautifulSoup(xml_content, 'lxml-xml')

    # 任务1
    root_tag = soup.find('Lockscreen')
    if root_tag:
        root_tag.name = 'Widget'
        root_tag['version'] = '2'
        root_tag['frameRate'] = '0'
        root_tag['screenWidth'] = '1080'
        root_tag.attrs.pop('screenHeight', None)
        root_tag.attrs.pop('displayDesktop', None)

    # 任务2
    ani_frame_tag = soup.find('AniFrame', {'time': '1876461209000'})
    if ani_frame_tag:
        ani_frame_tag.decompose()

    # 任务3
    for tag in soup.find_all(attrs={'disabled': 'miui'}):
        tag['disabled'] = '0'

    # 任务4
    soup = BeautifulSoup(str(soup).replace('_miui_', ''), 'lxml-xml')
    soup = BeautifulSoup(str(soup).replace('0.96*#s[1]', '#s[0]'), 'lxml-xml')

    # 任务5
    harmony_tags = soup.find_all('ExternalCommands', {'_harmony_': True})
    for harmony_tag in harmony_tags:
        harmony_tag.decompose()

    # 任务6
    i_hidden_tags = soup.find_all('i_Hidden')
    for i_hidden_tag in i_hidden_tags:
        i_hidden_tag.unwrap()

    # view_width, view_height
    for view_var_tags in soup.find_all('Var'):
        if 'view_width' == str(view_var_tags.get('name')) or 'view_height' == str(view_var_tags.get('name')):
            view_var_tags.decompose()

    # 将BeautifulSoup对象转换回XML字符串，使用prettify方法格式化XML
    modified_xml = str(soup.prettify(indent_width=4)).replace('    ', '\t')

    # 任务7（保存并替换原来的maml.xml）
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_xml)


def find_maml_files(directory):
    maml_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('maml.xml'):
                maml_files.append(os.path.join(root, file))
    return maml_files


if __name__ == "__main__":
    # 获取传入的目录路径
    input_directory = pyperclip.paste()

    # 遍历目录中的所有maml.xml文件
    maml_files = find_maml_files(input_directory)

    for maml_file in maml_files:
        # 读取每个maml.xml文件的内容
        with open(maml_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()

        # 处理XML内容
        process_maml_xml(xml_content, maml_file)
        order.orderXML(maml_file)
