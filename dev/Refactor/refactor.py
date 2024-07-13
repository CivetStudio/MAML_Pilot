import os.path
import re
import string
import random
import sys
import time

import pyperclip
from lxml import etree
import zlib
import bz2
# import base64

comment_1 = "欢迎定制锁屏：灵貓 QQ 1876461209  /  Welcome to customize the lock screen: Civet QQ 1876461209"
comment_2 = "违规抄袭将依据《中华人民共和国民法典》追究法律责任  /  Illegal plagiarism will be investigated for legal liability in accordance with the Civil Code of the People's Republic of China."


# def aes_encode(text):
#     encoded_bytes = base64.b64encode(text.encode('utf-8'))
#     hex_encoded = encoded_bytes.hex()
#     return hex_encoded
#
#
# def aes_decode(encoded_text):
#     decoded_bytes = bytes.fromhex(encoded_text)
#     decoded_text = base64.b64decode(decoded_bytes).decode('utf-8')
#     return decoded_text

def aes_encode(data):
    # data = data.replace(' ', '')
    compressed_data = bz2.compress(data.encode('utf-8'))
    # 将压缩后的数据转换为十六进制表示
    compressed_data_hex = compressed_data.hex()
    return compressed_data_hex


def aes_decode(compressed_data_hex):
    # 将十六进制表示的数据转换为压缩后的数据
    compressed_data = bytes.fromhex(compressed_data_hex)
    # 使用 bz2 模块进行解压缩
    decompressed_data = bz2.decompress(compressed_data).decode('utf-8')
    return decompressed_data

# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
# pip install pycrypto

# def aes_encode(text, key=b'\xae\xa2\xf7\xa8\xd4g\x1f\xc9\xf9\xf8~\x8e\t\xeb5\xec'):
#     cipher = AES.new(key, AES.MODE_CBC)
#     ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
#     iv = cipher.iv
#     return (iv + ct_bytes).hex()  # 将字节序列转换为十六进制字符串
#
#
# def aes_decode(ciphertext, key=b'\xae\xa2\xf7\xa8\xd4g\x1f\xc9\xf9\xf8~\x8e\t\xeb5\xec'):
#     ciphertext = bytes.fromhex(eval(ciphertext))  # 将十六进制字符串转换为字节序列
#     iv = ciphertext[:AES.block_size]
#     ciphertext = ciphertext[AES.block_size:]
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
#     return plaintext.decode('utf-8')


def get_xml_variable(file):
    global var_forbid_global
    global var_from_xml

    # 读取XML文件
    # tree = etree.parse(file)
    # root = tree.getroot()
    if os.path.exists(file):  # 如果输入是文件路径
        root = etree.parse(file)
    else:  # 如果输入是字符串
        file = '<ROOT>' + file + '</ROOT>'
        root = etree.fromstring(str(file))

    # 用于保存从XML中提取的变量名
    var_forbid_global = []
    var_from_xml = []

    # 找出包含【name=""】的标签
    for tag in root.xpath('//*[@name]'):
        name = tag.get('name')
        name_re = f'#{name}['
        root_str = etree.tostring(root, encoding='utf-8', pretty_print=True).decode('utf-8')
        # print(name_re, root_str)

        if name_re not in root_str:
            if name and name != '' and tag.tag != "Extra" and not name.startswith("$") and not name.endswith("$"):
                if tag.tag == 'ValueHolder' and tag.get('type') != 'string':
                    # 当 type 不是 string 时，将其属性名加入混淆
                    var_from_xml.append(name)
                elif tag.tag != 'ValueHolder':
                    var_from_xml.append(name)
            if tag.get('globalPersist') or tag.get('_glb') or tag.get('name').startswith('cur_'):
                var_forbid_global.append(name)
                # print(f"\t globalPersist: {name}")
                var_from_xml = list(set(var_from_xml))

    # 找出包含【dependency=""】的标签
    for tag in root.xpath('//*[@dependency]'):
        dependency = tag.get('dependency')
        if dependency and dependency != '' and tag.tag != "Extra" and not dependency.startswith(
                "$") and not dependency.endswith("$"):
            var_from_xml.append(dependency)
            var_from_xml = list(set(var_from_xml))

    # 找出包含【indexName=""】的标签
    for tag in root.xpath('//*[@indexName]'):
        index_name = tag.get('indexName')
        if index_name and index_name != '':
            var_from_xml.append(index_name)
            var_from_xml = list(set(var_from_xml))

    # 找出包含【countName=""】的标签
    for tag in root.xpath('//*[@countName]'):
        count_name = tag.get('countName')
        if count_name and count_name != '':
            var_from_xml.append(count_name)
            var_from_xml = list(set(var_from_xml))

    # print(var_from_xml)
    # time.sleep(1000)

    # 找出包含【target=""】的标签
    for tag in root.xpath('//*[@target]'):
        target = tag.get('target').replace('.visibility', '').replace('.animation', '')
        # print(target, len(var_from_xml), var_from_xml)
        # time.sleep(1000)
        # if len(var_from_xml) > 0:
        #     for i in range(len(var_from_xml)):
        #         print(var_from_xml)
        #         if target != var_from_xml[i] and len(target) >= 0:
        var_from_xml.append(target)
        var_from_xml = list(set(var_from_xml))

    var_from_xml.sort(key=lambda x: (len(x), x), reverse=True)
    return var_from_xml


def get_xml_content(file, var_forbid_list=[]):
    # 读取 XML 文件
    tree = etree.parse(file)

    # 获取整个 XML 树的完整文本（UTF-8 编码）
    full_text = etree.tostring(tree, method="xml", encoding="utf-8").decode('utf-8')

    return full_text


def xml_var_alias(input_xml, content, is_library_mode=0, var_forbid_list=[], suffix=None):
    global var_alias_dict
    global _callback

    _callback = ''

    def custom_encrypt(input_string, k=2, m='m', crc32_mode=1):
        if input_string in var_forbid_list or input_string in var_forbid_global:
            return input_string
        else:
            if crc32_mode:
                alias_dom_concat = m + hex(zlib.crc32(str(input_string).encode('UTF-8')))[2:].capitalize()
                alias_dom_hex = m if len(alias_dom_concat) == 8 else ''
                alias_str_new = str(alias_dom_concat + alias_dom_hex)
                return alias_str_new
            else:
                encrypted_string = random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=max(k, 2))
                encrypted_string = m + ''.join(encrypted_string)
                return encrypted_string

    var_from_target = get_xml_variable(input_xml)
    # random_8_digit = custom_encrypt('CIVET', 4, '').lower()
    random_8_digit = custom_encrypt(int(time.time() * 1000), 4, '').lower()

    var_alias_dict = {}

    for _i in range(len(var_from_target)):
        initial = str(var_from_target[_i])
        if initial not in var_forbid_list:
            if is_library_mode == 0:
                # 正常加密
                after = custom_encrypt(initial, 8, 'm')
                _callback = ''
            elif is_library_mode == 1:
                # 随机字符串
                after = initial + '_' + random_8_digit[:6]
                _callback = random_8_digit[:6]
            elif is_library_mode == 2:
                # 添加后缀
                after = initial + str(suffix)
                _callback = suffix
                # print('_callback', _callback)
            elif is_library_mode == 3:
                # 添加前缀
                after = str(suffix) + initial
            var_alias_dict[after] = initial

            # 将 initial 和 after 添加到字典中

            content = (
                content
                .replace(' name="' + initial + '"', ' name="' + after + '"')
                .replace(' target="' + initial + '"', ' target="' + after + '"')
                .replace(' dependency="' + initial + '"', ' dependency="' + after + '"')
                .replace(' indexName="' + initial + '"', ' indexName="' + after + '"')
                .replace(' countName="' + initial + '"', ' countName="' + after + '"')
                .replace(' src="' + initial + '.artwork"', ' src="' + after + '.artwork"')
                .replace(' strPara="' + initial + '"', ' strPara="' + after + '"')
                .replace('#' + initial + '"', '#' + after + '"')
                .replace('@' + initial + '"', '@' + after + '"')
                .replace('#' + initial + ')', '#' + after + ')')
                .replace('#' + initial + '+', '#' + after + '+')
                .replace('#' + initial + '-', '#' + after + '-')
                .replace('#' + initial + '*', '#' + after + '*')
                .replace('#' + initial + '/', '#' + after + '/')
                .replace('#' + initial + '%', '#' + after + '%')
                .replace('#' + initial + '=', '#' + after + '=')
                .replace('@' + initial + '=', '@' + after + '=')
                .replace('#' + initial + '}', '#' + after + '}')
                .replace('@' + initial + '}', '@' + after + '}')
                .replace('#' + initial + '{', '#' + after + '{')
                .replace('@' + initial + '{', '@' + after + '{')
                .replace('#' + initial + '!', '#' + after + '!')
                .replace('@' + initial + '!', '@' + after + '!')
                .replace('#' + initial + '[', '#' + after + '[')
                .replace('@' + initial + '[', '@' + after + '[')
                .replace('[#' + initial + ']', '[#' + after + ']')
                .replace('[@' + initial + ']', '[@' + after + ']')
                # .replace('[#' + initial, '[#' + after)
                # .replace('[@' + initial, '[@' + after)
                .replace('#' + initial + ']', '#' + after + ']')
                .replace('@' + initial + ']', '@' + after + ']')
                .replace('#' + initial + ',', '#' + after + ',')
                .replace('#' + initial + '.', '#' + after + '.')
                .replace('#' + initial + ' ', '#' + after + ' ')
                .replace('@' + initial + ')', '@' + after + ')')
                .replace('@' + initial + '+', '@' + after + '+')
                .replace('@' + initial + ',', '@' + after + ',')
                .replace('@' + initial + '.', '@' + after + '.')
                .replace('@' + initial + ' ', '@' + after + ' ')
                .replace(' src="' + initial + '"', ' src="' + after + '"')
                .replace('"' + initial + '.animation', '"' + after + '.animation')
                .replace('"' + initial + '.visibility', '"' + after + '.visibility')
            )

    # 创建根元素
    root = etree.Element("AntiAliasing", version="1")
    # 遍历字典中的键值对，创建子元素
    for initial, after in var_alias_dict.items():
        aliasing = etree.SubElement(root, "Aliasing", initial=after, after=initial)
    # 创建 XML 树
    tree = etree.ElementTree(root)

    # 将 XML 树写入文件
    tree.write(anti_xml, pretty_print=True, xml_declaration=True, encoding="utf-8")

    return content


def content_to_xml(content, modified_xml):
    # 解析 XML 字符串
    root = etree.fromstring(content.encode('utf-8'))  # 将 Unicode 字符串转换为字节串并解析

    # 对 XML 进行修改，例如添加新元素、修改属性等操作

    # 删除 globalPersist 变量的 persist 属性
    for p in root.xpath('//Var[@globalPersist="true"]'):
        for v in root.xpath(f'//VariableCommand[@name="{p.get("name")}"]'):
            if 'persist' in v.attrib:
                del v.attrib['persist']

    modified_content = etree.tostring(root, encoding="utf-8", pretty_print=True, xml_declaration=True).decode('utf-8')

    start_tag = etree.Element("Start")
    ends_tag = etree.Element("End")
    # 创建两条注释
    if comment_1:
        comment1 = etree.Comment(comment_1)
    if comment_2:
        comment2 = etree.Comment(comment_2)

    # 将修改后的 XML 字符串转换为 XML 元素
    modified_global = re.sub(r'\$(.*?)\$', r'\1', modified_content).encode('utf-8')
    modified_root = etree.fromstring(modified_global)  # 将 Unicode 字符串转换为字节串并解析

    # 在根元素之前插入两个注释
    try:
        # modified_root[1].addprevious(start_tag)
        # modified_root[-1].addnext(ends_tag)

        modified_root[1].addprevious(comment1)
        modified_root[1].addprevious(comment2)
    except Exception:
        pass

    # 创建 XML 树
    modified_tree = etree.ElementTree(modified_root)

    # 将修改后的 XML 写入文件
    modified_tree.write(modified_xml, pretty_print=True, xml_declaration=True, encoding="utf-8")


# 处理 XML 内容
def refactor(input_xml, is_library_mode=0, var_forbid_list=[], suffix='', output_xml=None):
    global _callback
    content = get_xml_content(input_xml, var_forbid_list)
    content = xml_var_alias(input_xml, content, is_library_mode, var_forbid_list, suffix)
    if output_xml is None:
        output_xml = input_xml
    content_to_xml(content, output_xml)
    # _callback: may be sufix / prefix
    return _callback.replace('_', '')


def get_var_alias_dict(_anti_xml):
    # 解析XML文件
    tree = etree.parse(_anti_xml)
    root = tree.getroot()

    # 初始化空字典
    _var_alias_dict = {}

    # 遍历子元素，提取变量名和别名
    for aliasing in root.iter("Aliasing"):
        initial = aliasing.get("after")
        after = aliasing.get("initial")
        _var_alias_dict[initial] = after

    return _var_alias_dict


def main():
    import time
    name = "[DEV_MODE]\nWELCOME TO REFACTOR.PY!"
    encode = aes_encode(name)[20:]
    length = len(encode)
    decode = aes_decode('425a6839314159265359' + encode)
    print(decode)
    print(f'{length}: {encode}')


if __name__ == "__main__":

    main()

    comment_1 = ""
    comment_2 = ""
    maml_xml = './../../lib/BattImage/4digit.e.xml'
    save_xml = './../../lib/BattImage/4digit.f.xml'
    anti_xml = os.path.join(os.path.dirname(maml_xml), 'anti.xml')
    var_forbid_name = ['']
    refactor(maml_xml, 3, var_forbid_name, 'kbd_', save_xml)

    # XML 文件路径
    # maml_xml = '/Users/wangshilong/Desktop/导出/MAMLPilot/dev/Refactor/advance/source.xml'
    # save_xml = os.path.join(os.path.dirname(maml_xml), 'new.xml')
    # anti_xml = os.path.join(os.path.dirname(maml_xml), 'anti.xml')
    # var_forbid_name = ['']
    # refactor(maml_xml, 0, var_forbid_name, save_xml)
    # print(var_from_xml)
    # print(var_forbid_global)

else:
    # maml_xml = pyperclip.paste().strip()
    anti_xml = 'anti.xml'
