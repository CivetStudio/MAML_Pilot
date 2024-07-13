import pyperclip
from bs4 import BeautifulSoup
from dev.Refactor.Var.var_forbid import var_forbid_name as vfb
from dev.Refactor.refactor import get_xml_variable
from collections import defaultdict
from tools.xsd import main as xsd


todo = {
    '当前标签下无该属性',
    '属性重复',
    '结构错误',
    '文件头未从首字符开始',
    '<或</后不能为空',
    '代码不完整',
    '空值',
    '文件头只能<>结构',
    '后单引号缺失',
    '数组后才能有 [ ] ',
    ')]多或前面([缺失',
    ',号只能在函数表达式内',
    ')]缺失或前面([多',
    '函数式内元素个数有误',
    '变量名错误',
    '此变量名从未声明',
    '函数名后只能为（',
    '单个xml只能有一个VariableBinders或者ExternalCommands',
    '函数名错误或无#@',
    '运算符错误',
    '运算符位置错误',
    '小数点多了',
    '数字内有空格',
    '数组名有小数点',
    '（前不可以是数字和变量',
    '数组名有空格',
}


BLACK = "\033[37m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"


def short_desc(context):
    print(context)


def print_with_ansi_colors():
    colors = {
        "Black": "\033[30m",
        "Red": "\033[31m",
        "Green": "\033[32m",
        "Yellow": "\033[33m",
        "Blue": "\033[34m",
        "Purple": "\033[35m",
        "Cyan": "\033[36m",
        "White": "\033[37m",
        "Bright Black (Gray)": "\033[90m",
        "Bright Red": "\033[91m",
        "Bright Green": "\033[92m",
        "Bright Yellow": "\033[93m",
        "Bright Blue": "\033[94m",
        "Bright Purple": "\033[95m",
        "Bright Cyan": "\033[96m",
        "Bright White": "\033[97m",
    }

    reset = "\033[0m"

    for color_name, color_code in colors.items():
        print(f"{color_code}{color_name}{reset}")
    print('\t')


def main(soup_xml):
    result = []
    line = '行'

    def get_line_number(file_path, target_str):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                if target_str in line:
                    return i
        return None

    def check_tag_print(_tag, _tag_name, _attr, _extra, _print, _has_value=1, _has_line=1):
        _value = _tag.get(_attr)

        if _tag.name == _tag_name:
            if attr == _attr and eval(_extra) == 1:
                if _has_line:
                    line_ = f'{line} {line_number}: '
                print_ = line_ + _print
                if _has_value:
                    print_ += f' ===> {_attr}="{_value}"'
                result.append(BLACK + print_ + RESET)

    # 解析 XML
    soup = BeautifulSoup(open(soup_xml), 'xml')

    # 查找所有具有属性的标签
    tags_with_attrs = soup.find_all(True)

    # 检查每个标签的属性
    for tag in tags_with_attrs:

        if tag.name == 'Lockscreen':
            _value = tag.get('frameRate')
            if not (_value.isdigit() and int(_value) >= 0):
                result.append(f'{RED}根标签帧率frameRate设置错误{RESET}')

        if tag.name == 'Var':
            tag_info = {}
            for attr, value in tag.attrs.items():
                tag_info[attr] = value
            if not tag.get('name'):
                result.append(f'{BLACK}发现未定义name的Var标签: {tag_info}{RESET}')
            else:
                if tag['name'] in vfb and tag['name'] not in ['notification', 'shake_record']:
                    if tag['name'].startswith('Weather') and tag.parent.name == 'Weather':
                        pass
                    else:
                        result.append(f'''{CYAN}变量名称与系统变量冲突: name="{tag.get('name')}"{RESET}''')
                if '#' + tag['name'] in str(tag.get('expression')) and 'isnull' not in str(tag.get('expression')):
                    result.append(f'''{RED}发现循环调用name的Var标签: {tag_info}{RESET}''')

        if tag.name == 'SensorBinder':
            if tag.parent and tag.parent.name != 'VariableBinders':
                short_desc(f'{RED}父级不包含该标签{RESET}')
                result.append(f'{RED}暂不支持SensorBinder标签，请检查该标签位置及拼写是否正确{RESET}')

    # 初始化一个字典来存储不同标签下的属性值
    attribute_values_by_tag = defaultdict(list)
    attribute_name = 'name'

    # 查找所有具有指定属性名的标签
    tags_with_attribute = soup.find_all(attrs={attribute_name: True})

    # 将属性值按标签名称分类存储
    for tag in tags_with_attribute:
        tag_name = tag.name
        attribute_values = tag.get(attribute_name)
        attribute_values_by_tag[tag_name].append(attribute_values)

    # 检测重复的属性值
    for tag_name, attribute_values in attribute_values_by_tag.items():
        if tag_name not in ['List', 'Extra'] and not tag_name.endswith('Command'):
            counter = defaultdict(int)
            for value in attribute_values:
                counter[value] += 1
            for value, count in counter.items():
                if count > 1:
                    result.append(f'{CYAN}正在重复定义 {tag_name} ===> {attribute_name}="{value}", 重复次数: {count}{RESET}')

    var_from_xml = get_xml_variable(soup_xml)
    # print(var_from_xml)

    # 检查每个标签的属性
    for tag in tags_with_attrs:

        for attr, value in tag.attrs.items():

            line_number = get_line_number(soup_xml, f'{attr}="{value}"')
            check_tag_print(tag, "VariableAnimation", "delay", "int(_value) < 0", "基础动效delay属性必须为数值且大于等于0")
            check_tag_print(tag, "VariableAnimation", "repeat", "int(_value) < 0", "基础动效repeat属性必须为数值且大于等于0")
            check_tag_print(tag, "VarArray", "type", "_value not in['number', 'string']", "VarArray标签的type类型有误")
            check_tag_print(tag, "Text", "shadow", "_value.count('|') != 3", "文本标签shadow属性错误")
            check_tag_print(tag, "Text", "format", "'##' in str(_value) or '%' not in str(_value)", "文本标签format属性错误")
            check_tag_print(tag, "DateTime", "format", "'##' not in str(_value)", "日期标签format属性错误")

            sensor_type = f'''"{tag.parent.get('type', '')}"'''
            check_tag_print(tag, "Variable", "index", "_tag.parent.name == 'SensorBinder' and not _value.isdigit()", f"SensorBinder标签type={sensor_type}里的index值必须为数值")
            check_tag_print(tag, "Variable", "index", "_tag.parent.name == 'SensorBinder' and _value.isdigit() and int(_value) > 2", f"SensorBinder标签type={sensor_type}里的index值超出范围")
            check_tag_print(tag, "Var", "mode", "_tag.get('name') == 'Progress' and (int(_value) > 4 or int(_value) < 0)", '进度条Var="Progress"的mode的值需在0-4之间，否则无效')

            # 检查属性值中括号的完整性
            left_count = value.count('(')
            right_count = value.count(')')
            if left_count != right_count:
                result.append(f'{RED}{line} {line_number}: 括号不完整 ===> {attr}="{value}"{RESET}')
            else:
                pass

            # 字符解析错误: {_value} 提示：变量前面请加#或@，字符串请加单引号
            for i in range(len(var_from_xml)):
                if var_from_xml[i] in value:
                    index = value.index(var_from_xml[i])
                    if index > 0:
                        prefix = value[index - 1]
                        if prefix in ['+', '-', '*', '/', '%', '(', ')'] and attr not in ['column', 'columns', 'uri', 'data', 'action', 'name', 'src', 'srcExp', 'srcFormat']:
                            # if prefix not in ["#", "@", "'", "/", "_"] and attr not in ['column', 'columns', 'uri', 'data', 'action', 'name', 'src']:
                            result.append(f'{RED}{line} {line_number}: 字符解析错误: {prefix + var_from_xml[i]} 提示：变量前面请加#或@，字符串请加单引号 ===> {attr}="{value}"{RESET}')

    return result


if __name__ == '__main__':
    # print_with_ansi_colors()
    soup_xml = './xsd/xsd_error.xml'
    # soup_xml = pyperclip.paste()

if xsd(soup_xml):
    xsd_result = xsd(soup_xml)
result = main(soup_xml)
if result:
    for r in result:
        print(r)
else:
    print('[attrition] XML syntax is valid.')


# if tag.name == 'VariableAnimation':
#     if attr == 'delay' and int(value) < 0:
#         print(f'基础动效delay属性必须为数值且大于等于0: {value}, line {line_number}')
#
#     if attr == 'repeat' and int(value) < 0:
#         print(f'基础动效repeat属性必须为数值且大于等于0: {value}, line {line_number}')
#
# if tag.name == 'VarArray':
#     if attr == 'type' and ['number', 'string'] != value:
#         print(f'VarArray标签的type类型有误: line {line_number}')
#
# if tag.name == 'Text':
#     if attr == 'shadow':
#         print(f'文本标签shadow属性错误: line {line_number}')

# print(f'Unbalanced parentheses in attribute: {attr}={value} in tag <{tag.name}>')
