import os
import sys
import pyperclip
from lxml import etree
from bs4 import BeautifulSoup
import re

# import zlib

orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


BeautifulSoup.prettify = prettify


def process_xml_xiaomi(process_xml):
    soup = BeautifulSoup(open(process_xml), 'lxml-xml')
    lockscreen = soup.Lockscreen
    external_commands = soup.Lockscreen.ExternalCommands
    # print(external_commands)

    if 'disableChargeAnim' not in str(soup) and 'battery_' in str(soup):
        trigger_binder = soup.new_tag('Trigger')
        trigger_binder['action'] = 'resume,pause,init'
        trigger_content = '''
        <ExternCommand command="disableChargeAnim" numPara="1" />
        '''
        trigger_content = BeautifulSoup(trigger_content, 'lxml-xml')
        trigger_binder.append(trigger_content)
        # 若无 ExternalCommands 标签，则手动创建
        if not soup.Lockscreen.ExternalCommands:
            new_external_commands = soup.new_tag('ExternalCommands')
            new_external_commands.append(trigger_binder)
            print('\t', new_external_commands)
            lockscreen.append(new_external_commands)
        else:
            external_commands.append(trigger_binder)

    for var in soup.find_all('Var'):
        var_name = var.get('name')
        var_exp = var.get('expression')
        var_type = var.get('type', 'number')
        var_char = '#'
        if var_type == 'string':
            var_char = '@'
        if var_exp and (var_exp.isdigit() or var.get('_const')):
            var['expression'] = f'ifelse(isnull({var_char}{var_name}),{var_exp},{var_char}{var_name})'
            print(f"\t {var['expression']}")

    # intentMarket() from splitTools.py and Optimized
    IntentCommand = 0
    for i in soup.find_all('IntentCommand'):
        IntentCommand += 1
        # 第三方APP自动跳转商店
        intent_package = str(i.get('package'))
        intent_class = str(i.get('class'))
        if not intent_package.startswith(('com.android', 'com.huawei', 'com.example.android.notepad', 'com.coloros',
                                          'com.oppo', 'com.nearme', 'com.heytap', 'com.oplus', 'com.miui', 'com.vivo',
                                          'com.bbk', 'com.iqoo', 'com.hihonor', 'oppo.multimedia', 'com.xiaomi.market')) \
                and str(i.get('action')).upper() == 'ANDROID.INTENT.ACTION.MAIN' \
                and i.get('package') and i.get('class'):
            pkg_var_exp = intent_package
            cls_var_exp = intent_class
            # print(
            #     f"\t {i}: <IntentCommand action=\"{i.get('action')}\" package=\"{pkg_var_exp}\" class=\"{cls_var_exp}\" />")

            origin_condition = str(i.get('condition')) if i.get('condition') is not None else '1'
            multi_command = f'''<IntentCommand condition="{origin_condition}" action="android.intent.action.VIEW" uriExp="'mimarket://launchordetail?id={pkg_var_exp}'" />'''
            print(f'\t {multi_command}')
            multi_soup = BeautifulSoup(multi_command, 'lxml-xml')
            i.insert_before(multi_soup)

    for video in soup.find_all('Video'):
        video.extract()

    with open(process_xml, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify(indent_width=4).replace('    ', '\t')))


# 示例用法
if __name__ == '__main__':

    maml_main_xml = pyperclip.paste().replace('\\', '/').replace('"', '')

    maml_rule_file = ".xml"
    maml_file_name = os.path.basename(maml_main_xml)

    # 判断 maml_file_name 是否以 maml_rule_file 结尾
    if maml_rule_file not in maml_file_name:
        print(f"Error: File must be '{maml_rule_file}'")
        sys.exit(1)

    print('\t')
    print(f'Source: {maml_main_xml}\n')

    process_xml_xiaomi(maml_main_xml)
