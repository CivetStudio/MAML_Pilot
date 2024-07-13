import os
import sys
import pyperclip
from lxml import etree
from bs4 import BeautifulSoup
import re

orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


BeautifulSoup.prettify = prettify


def get_line_number(file_path, target_str):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            if target_str in line:
                return i
    return None


def detect_lockscreen_view(process_xml):
    parser = etree.XMLParser(recover=True)
    # noinspection PyTypeChecker
    tree = etree.parse(process_xml, parser)
    root = tree.getroot()

    for elem in root.iter():
        if elem.tag in ['VariableCommand', 'Var']:
            if 'type' in elem.attrib:
                del elem.attrib['type']

        if elem.tag in ['Text', 'APNG', 'DateTime', 'VibrateCommand', 'ParticleCommand',
                        'CollBodyCommand', 'Calendar', 'EditText', 'CollisionWorld',
                        'PressingAPNGView', 'FluidsView', 'StereDropView', 'ARBase', 'Layer']:
            print(
                f"\t Found <{elem.tag} /> at line {elem.sourceline}: {etree.tostring(elem, encoding='utf-8').decode('utf-8').strip()}")

            # 处理 Text 标签
            if elem.tag == 'Text':
                for attr in ['scrollDisplay', 'marqueeRepeatLimit', 'clickable', 'delayTime']:
                    if attr in elem.attrib:
                        print(f"  Removing attribute {attr}")
                        del elem.attrib[attr]

            # 处理 DateTime 标签
            # if elem.tag == 'DateTime':
            #     elem.tag = 'Text'
            #     elem.attrib['paras'] = f"formatDate('{elem.attrib['format']}',@time_sys)"
            #     elem.attrib['format'] = '%s'
            #     del elem.attrib['value']
            #     print(f"  Refactoring <{elem.tag} />: {etree.tostring(elem, encoding='utf-8').decode('utf-8').strip()}")

            # 删除不支持的标签
            elif elem.tag != 'DateTime' and elem.tag != 'Text':
                print(f"  Removing <{elem.tag} />")
                elem.getparent().remove(elem)

            # print('\t')

    tree.write(process_xml, encoding="utf-8", xml_declaration=True)


def process_lockscreen_var(process_xml):
    soup = BeautifulSoup(open(process_xml), 'lxml-xml')
    start_tag = soup.new_tag('Start')
    lockscreen = soup.Lockscreen
    lockscreen.insert(1, start_tag)

    if 'name="isHonor"' not in str(soup):
        is_honor = soup.new_tag('Var', attrs={'name': 'isHonor', 'expression': '1'})
        lockscreen.append(is_honor)

    for var in soup.find_all('Var'):
        if var.get('name') == 'isHonor':
            var['expression'] = '1'

    var_procress_honor = 0 if str(lockscreen.get('_processHonorVar')).upper() == "FALSE" or lockscreen.get(
        '_processHonorVar') == "0" else 1
    print(f'Root[_processHonorVar]: {var_procress_honor}')

    if var_procress_honor:
        for tag in soup.find_all('VariableCommand'):
            # 获取 VariableCommand 属性
            if (tag.parent.name == 'Trigger' and not tag.parent.parent.get('threshold')) or \
                    tag.parent.parent.name == 'ExternalCommands':
                var_comp_name = tag.get('name')
                var_comp_exp = tag.get('expression')
                var_comp_type = tag.get('type')

                var_comp_persist = 'false' if tag.get('persist') is None else 'true'

                # 输出同名变量
                for var in soup.find_all('Var'):
                    if var['name'] == var_comp_name and var.get('expression') and var['expression'] != var_comp_exp and var.get('index') is None and _DEBUG_:
                        print(var, var_comp_exp)

                # 查询是否有同名的 Var 变量
                var_tag_form = bool(soup.find_all('Var', attrs={'name': var_comp_name}) != [])

                if not var_tag_form:
                    if _DEBUG_:
                        print(f'<Var name="{var_comp_name}" expression="{var_comp_exp}" />')
                    if var_comp_persist == 'false':
                        new_var_honor = soup.new_tag('Var', attrs={'name': var_comp_name, 'expression': var_comp_exp, 'type': var_comp_type})
                    else:
                        new_var_honor = soup.new_tag('Var', attrs={'name': var_comp_name, 'expression': var_comp_exp, 'type': var_comp_type, 'persist': var_comp_persist})
                    if 'rand()' in var_comp_exp:
                        new_var_honor['const'] = 'true'
                    soup.Lockscreen.append(new_var_honor)

    for intent in soup.find_all('IntentCommand'):
        package_name = intent.get('package')
        class_name = intent.get('class')
        if str(package_name).startswith('com.huawei.') or str(class_name).startswith('com.huawei.') \
                or (str(package_name) == 'com.android.deskclock' and str(class_name) == 'com.android.deskclock.AlarmsMainActivity') \
                or (str(package_name) == 'com.android.calendar' and str(class_name) == 'com.android.calendar.AllInOneActivity') \
                or (str(package_name) == 'com.android.mms' and str(class_name) == 'com.android.mms.ui.ConversationList')\
                or (str(package_name) == 'com.android.calculator2' and str(class_name) == 'com.android.calculator2.Calculator')\
                or (str(package_name) == 'com.android.contacts')\
                or (str(package_name) == 'com.android.email')\
                or (str(package_name) == 'com.example.android.notepad')\
                or (str(package_name) == 'com.android.soundrecorder')\
                or (str(package_name) == 'com.vmall.client')\
                or 'huawei' in str(package_name) or 'huawei' in str(class_name):
            intent.extract()
        else:
            if intent.get('category'):
                del intent['category']

    for var in soup.find_all('Var'):
        if var.get('_honor') is None:
            if var.get('index') is not None and var.parent.name == soup.name and _DEBUG_:
                print(var)
            var_name = var.get('name')
            var_exp = var.get('expression')
            var_filter_0 = f"#{str(var_name)}+1"
            var_filter_1 = f"not(#{str(var_name)})"
            if var_exp and (var_filter_0 in str(var_exp) or var_filter_1 in str(var_exp)):
                if _DEBUG_:
                    print("Loop:", var)
                var['expression'] = '0'
            if f'#{var_name}' in str(soup):
                var['type'] = 'number'
            elif f'@{var_name}' in str(soup):
                var['type'] = 'string'
            else:
                var['type'] = 'number'

            # if lockscreen.ExternalCommands:
            #     lockscreen.ExternalCommands.insert_after(var)
            # else:
            #     start_tag.insert_after(var)

    start_tag.decompose()

    with open(process_xml, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify(indent_width=4).replace('    ', '\t').replace('@_description', '@Weather.today.weatherIconDes').replace('ifelse(ne(#LangsId,2),#time+#time_sys,round(#S_TimeLoop))', '#time')))


# 示例用法
if __name__ == '__main__':

    _DEBUG_ = 1

    maml_main_xml = pyperclip.paste().replace('\\', '/').replace('"', '')

    maml_rule_file = ".xml"
    maml_file_name = os.path.basename(maml_main_xml)

    # 判断 maml_file_name 是否以 maml_rule_file 结尾
    if maml_rule_file not in maml_file_name:
        print(f"Error: File must be '{maml_rule_file}'")
        sys.exit(1)

    print('\t')
    print(f'Source: {maml_main_xml}\n')

    detect_lockscreen_view(maml_main_xml)
    process_lockscreen_var(maml_main_xml)

else:
    _DEBUG_ = 0
# 查找变量内是否循环套用 <Var name="a" expression="#a+1" />
# 未知原因丢失 Var.type 属性
