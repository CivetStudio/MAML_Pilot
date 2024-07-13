import shutil
import sys
import os
import pyperclip
import subprocess
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


def search_xml_files(root_folder, search_string):
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.xml') and filename.startswith('i_'):
                file_path = os.path.join(foldername, filename)
                try:
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    # 搜索文件内容
                    if search_string in ET.tostring(root).decode('utf-8'):
                        # print("在文件 {} 中找到字符串 '{}'".format(file_path, search_string))
                        _return_ = os.path.basename(file_path)
                        return _return_

                except ET.ParseError:
                    print("无法解析文件:", file_path)


def find_manifest_xml_files(root_folder):
    manifest_files = []
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename == 'manifest.xml':
                file_path = os.path.join(foldername, filename)
                manifest_files.append(file_path)
    return manifest_files


def main(input_folder, double_check=0, lib_folder_name='lib'):
    # 传入路径自动查找 manifest.xml
    pyperclip_paste = find_manifest_xml_files(input_folder)

    for i in pyperclip_paste:
        if i.endswith('manifest.xml'):

            if double_check == 0:
                # source_xml = os.path.join(os.path.dirname(i), '..', 'source.xml')
                # shutil.copyfile(i, source_xml)
                maml_xml = os.path.join(os.path.dirname(i), 'maml.xml')
                shutil.copyfile(i, maml_xml)
                print(f'Source: {i}')
                # print(maml_xml)
                os.remove(i)
                soup = BeautifulSoup(open(maml_xml, encoding='utf-8'), 'lxml-xml')

                # For 屋里设计
                new_soup = str(soup).replace('(#month+1)', '#months')\
                    .replace('ifelse(eq(#hour12,0),1,#hour12/10)', '#hours12.0')\
                    .replace('ifelse(eq(#hour12,0),2,#hour12%10)', '#hours12.1')
                soup = BeautifulSoup(str(new_soup), 'lxml-xml')
                langs_id = soup.new_tag('Var', attrs={'name': 'LangsId', 'expression': '2'})
                months = soup.new_tag('Var', attrs={'name': 'months', 'expression': 'int(#month+1)'})
                hours12_0 = soup.new_tag('Var', attrs={'name': 'hours12.0', 'expression': 'ifelse(eq(#hour12,0),1,int(#hour12/10))'})
                hours12_1 = soup.new_tag('Var', attrs={'name': 'hours12.1', 'expression': 'ifelse(eq(#hour12,0),2,int(#hour12%10))'})
                soup.Lockscreen.append(langs_id)
                soup.Lockscreen.append(months)
                soup.Lockscreen.append(hours12_0)
                soup.Lockscreen.append(hours12_1)

                # intent 匹配库
                for intent in soup.find_all('IntentCommand'):
                    package = intent.get('class', 'None')
                    condition = intent.get('condition', '1')
                    if package != 'None':
                        intent_file_name = str(search_xml_files(lib_folder_name, package)).split('.xml')[0]
                        if intent_file_name != 'None':
                            intent_tag = soup.new_tag(intent_file_name, attrs={'condition': condition})
                            intent_info = f"{{'package': {intent.get('package')}, 'class': {intent.get('class')}}}"
                            print(intent_info, '->', intent_tag)
                            intent.insert_after(intent_tag)
                            intent.extract()
                print('\t')
                # print(soup)

                # 覆盖至 maml.xml
                with open(maml_xml, 'w', encoding='utf-8') as fb:
                    fb.write(str(soup.prettify()))

                # 处理 maml.xml
                pyperclip.copy(maml_xml)
                script_path = 'main.py'
                result = subprocess.run(['./venv/bin/python3', script_path], check=False, stdout=subprocess.DEVNULL)

                # 处理 manifest.xml
                pyperclip.copy(i)
                script_path = 'tools/honor.py'
                result = subprocess.run(['./venv/bin/python3', script_path], check=False, stdout=subprocess.DEVNULL)

                # 回收 maml.xml
                os.remove(maml_xml)

            # 寻找循环调用的Var
            if double_check == 1:
                manifest_xml = os.path.join(os.path.dirname(i), 'manifest.xml')
                print(f'Source: {i}')
                soup = BeautifulSoup(open(manifest_xml, encoding='utf-8'), 'lxml-xml')

                for var in soup.find_all('Var'):
                    var_name = var.get('name')
                    var_expression = var.get('expression')
                    var_concat = '#' + str(var_name)
                    if str(var_concat) in str(var_expression):
                        var['expression'] = '0'
                        print(var)
                print('\t')

                # 覆盖至 maml.xml
                with open(manifest_xml, 'w', encoding='utf-8') as fb:
                    fb.write(str(soup.prettify()))


if __name__ == '__main__':
    main(pyperclip.paste(), 1)
