import sys

from bs4 import BeautifulSoup
import zlib
import time
import re

# orig_prettify = BeautifulSoup.prettify
# r = re.compile(r'^(\s*)', re.MULTILINE)
# def prettify(self, encoding=None, formatter="minimal", indent_width=4):
#     return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))
# BeautifulSoup.prettify = prettify


def splitVar(parse_file, save_file):
    with open(parse_file, 'r', encoding='utf-8') as f:
        xml_str = f.read()
    soup = BeautifulSoup(xml_str, features="lxml-xml")

    lockscreen = soup.Lockscreen
    for group in lockscreen.find_all('Group'):
        # 10.06 BUG: Array > Group > Var
        if group.parent.name != 'Array':
            for var in group.find_all('Var'):
                if var.parent.name == "Group" and var.get('name') != 'Progress':
                    var.extract()
                    lockscreen.append(var)

    with open(save_file, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify(indent_width=4).replace('    ', '\t')))


def splitExt(save_file):
    # ExternalCommands
    with open(save_file, 'r', encoding='utf-8') as f:
        xml_str = f.read().replace('\n', '').replace('\t', '')
    soup = BeautifulSoup(xml_str, features="lxml-xml")

    # 查找所有的Trigger标签，并将它们按照action的值合并为一个字典
    trigger_dict = {}
    # trigger_content = []
    # content = ''

    # 移除所有alias属性
    widget_mode = 1 if 'version="10000"' in str(soup) else 0
    if not widget_mode:
        for tag in soup.find_all(alias=True):
            del tag['alias']

    for t in soup.find_all('Trigger'):
        if t.parent.name == "ExternalCommands":
            action = t['action']
            # for c in t.find_all(True):
            # content = str(c)
            ec_contents = [item for item in t.contents if item != '\n']
            # content = str(t.contents).replace('[', '').replace('],', '').replace(']', '').strip()
            content = str(ec_contents).replace('[', '').replace(']', '')
            if action not in trigger_dict:
                trigger_dict[action] = [content]
            else:
                trigger_dict[action].append(content)
            t.extract()

    # 新建ExternalCommands标签
    external_commands = soup.new_tag('ExternalCommands')

    # 将合并后的Trigger添加到ExternalCommands标签中
    for action, content in trigger_dict.items():
        t = soup.new_tag('Trigger', action=action)
        t.string = '\n'.join(content)
        external_commands.append(t)

    # 查找原来的ExternalCommands标签，并将它替换为新的ExternalCommands标签
    if soup.Lockscreen.ExternalCommands is not None:
        old_external_commands = soup.find_all('ExternalCommands')[0]
        # old_external_commands.replace_with(external_commands)
        old_external_commands.decompose()
        external_commands_str = str(external_commands).replace('&lt;', '<').replace('&gt;', '>').replace(", ' ',", "").replace("' ',", "").replace(", ' '", "")
        e_soup = BeautifulSoup(external_commands_str, features="lxml-xml")
        # print('e_soup:',e_soup)
        soup.Lockscreen.append(e_soup)

    # 输出到文件中
    with open(save_file, 'w', encoding='utf-8') as f:

        soup_str = str(
            soup.prettify(indent_width=4).replace('&lt;', '<').replace('&gt;', '>').replace('    ', '\t').replace(
                '<ExternalCommands>\n\t</ExternalCommands>\n', '').replace('<ExternalCommands/>\n', ''))
        soup = BeautifulSoup(soup_str, features="lxml-xml")
        f.write(str(soup.prettify(indent_width=4).replace('    ', '\t').replace(',\n', '')))


# f.write(str(soup.prettify(indent_width=4).replace('<ExternalCommands>\n\t</ExternalCommands>\n','').replace('<ExternalCommands/>\n','').replace('    ','\t')).replace('amp;gt;','gt;').replace('amp;lt;','lt;').replace('amp;amp;','amp;'))


def splitBinders(save_file):
    # VariableBinders
    with open(save_file, 'r', encoding='utf-8') as f:
        xml_str = f.read()
    soup = BeautifulSoup(xml_str, features="lxml-xml")

    merged_text = ''
    variable_binders = soup.Lockscreen.find_all('VariableBinders')
    for vb in variable_binders:
        # print(vb.comment)
        for i in range(len(vb.contents)):
            merged_text = merged_text + str(vb.contents[i])
    new_variable_binders = soup.new_tag('VariableBinders')
    new_variable_binders.string = merged_text
    for vb in variable_binders:
        vb.extract()
    soup.Lockscreen.append(new_variable_binders)

    for o in soup.find_all('VariableBinders'):
        # print(o.contents)
        if o.contents == ['']:
            o.decompose()

    # 输出到文件中
    with open(save_file, 'w', encoding='utf-8') as f:

        soup_str = str(soup.prettify(indent_width=4).replace('&lt;', '<').replace('&gt;', '>').replace('    ', '\t'))
        soup = BeautifulSoup(soup_str, features="lxml-xml")
        # f.write(str(soup.prettify(indent_width=4).replace('    ', '\t')))
        f.write(str(soup.prettify(indent_width=4).replace('    ', '\t').replace('amp;gt;', 'gt;').replace('amp;lt;',
                                                                                                          'lt;').replace(
            'amp;amp;', 'amp;')))


def preLoadVar(save_file):
    with open(save_file, 'r', encoding='utf-8') as f:
        xml_str = f.read()
    soup = BeautifulSoup(xml_str, features="lxml-xml")

    lockscreen = soup.Lockscreen
    for importer in lockscreen.find_all('Import'):
        importer.decompose()

    if lockscreen.Wallpaper is not None and lockscreen.Wallpaper.parent.name == 'Lockscreen':

        for var in lockscreen.find_all('Var'):
            # if var.parent != 'Weather' and var.parent != 'Calendar' and var.parent != 'Healthy' and var.parent != 'Array':
            if var.parent.name == 'Lockscreen' and var.parent.name != 'Array':
                var.extract()
                lockscreen.Wallpaper.insert_before(var)

        for var_animation in lockscreen.find_all('Var'):
            if var_animation.find("VariableAnimation"):
                var_animation.extract()
                lockscreen.Wallpaper.insert_before(var_animation)

        for var_threshold in lockscreen.find_all('Var'):
            if var_threshold.get("threshold") is not None:
                var_threshold.extract()
                lockscreen.Wallpaper.insert_before(var_threshold)

        for hw_weather in lockscreen.find_all('Weather'):
            hw_weather.extract()
            lockscreen.Wallpaper.insert_before(hw_weather)

        for hw_calendar in lockscreen.find_all('Calendar'):
            hw_calendar.extract()
            lockscreen.Wallpaper.insert_before(hw_calendar)

        for hw_healthy in lockscreen.find_all('Healthy'):
            hw_healthy.extract()
            lockscreen.Wallpaper.insert_before(hw_healthy)

        for var_array in lockscreen.find_all('VarArray'):
            var_array.extract()
            lockscreen.Wallpaper.insert_before(var_array)

        for countdown_time in lockscreen.find_all('CountDownTime'):
            countdown_time.extract()
            lockscreen.Wallpaper.insert_before(countdown_time)

    else:
        # Try to change mode into 'Lockscreen.Wallpaper' origin: 'Lockscreen.Image'
        print("Prompt: 'preLoadVar' canceled, missed of 'Lockscreen.Wallpaper'")

    with open(save_file, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify(indent_width=4).replace('    ', '\t')))


def preLoadExt(save_file):
    with open(save_file, 'r', encoding='utf-8') as f:
        xml_str = f.read()
    soup = BeautifulSoup(xml_str, features="lxml-xml")

    lockscreen = soup.Lockscreen
    for ext in lockscreen.find_all('ExternalCommands'):
        ext.extract()
        lockscreen.Var.insert_before(ext)

    for binders in lockscreen.find_all('VariableBinders'):
        binders.extract()
        if lockscreen.ExternalCommands is None:
            lockscreen.Var.insert_before(binders)
        else:
            lockscreen.ExternalCommands.insert_after(binders)

    with open(save_file, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify(indent_width=4).replace('    ', '\t')))


def evalNum(number):
    new_number = str(number)
    try:
        new_number = str(eval(number))
    except Exception:
        pass
    return str(new_number)


def splitGroup(manifest_xml, manifest_root):

    with open(manifest_xml, 'r', encoding='utf-8') as f:
        xml_str = f.read()

    # 解析xml文件
    soup = BeautifulSoup(xml_str, features="lxml-xml")
    button_str = []

    if manifest_root != 'Widget':

        # 检测/移除空属性
        for element in soup.find_all():
            # 遍历元素的所有属性
            for attr_name, attr_value in element.attrs.items():
                if attr_value == '' or str(attr_value).strip() == '':
                    print(f'⚠️Warning: {element}')
        time.sleep(1)
        print('\t')

        print('Button:')
        for button in soup.find_all('Button'):
            # if button.parent.name != 'Lockscreen' and button.parent.name == 'Group' and button.parent.name != 'Array' and button.parent.parent.name != 'Array' and button.parent.parent.parent.name != 'Array' and button.parent.parent.parent.parent.name != 'Array':
            if button.parent.name != 'Lockscreen' and button.parent.name == 'Group' and button.parent.name != 'Array' and button.parent.parent.name != 'Array' and button.parent.parent.parent.name != 'Array' and button.parent.name != 'Item' and button.parent.parent.name != 'List' and button.parent.name != 'MusicControl' and button.parent.parent.name != 'MusicControl' and button.parent.name != 'StereoGroup':

                # 第一层 Group标签
                group_x = '(' + button.parent.get('x', '0') + ')' + '+(' + button.get('x', '0') + ')'
                group_y = '(' + button.parent.get('y', '0') + ')' + '+(' + button.get('y', '0') + ')'
                group_visibility = '(' + button.parent.get('visibility', '1') + ')*(' + button.get('visibility','1') + ')'

                group_x = evalNum(group_x)
                group_y = evalNum(group_y)

                # 第二层 Group标签
                if button.parent.parent.name == 'Group':
                    # print('Secondary', '\n')
                    group_x = group_x + '+(' + evalNum(button.parent.parent.get('x', '0')) + ')'
                    group_y = group_y + '+(' + evalNum(button.parent.parent.get('y', '0')) + ')'
                    group_visibility = group_visibility + '*(' + button.parent.parent.get('visibility', '1') + ')'

                    group_x = evalNum(group_x)
                    group_y = evalNum(group_y)

                    # 第三层 Group标签
                    if button.parent.parent.parent.name == 'Group':
                        # print('Tertiary', '\n')
                        group_x = group_x + '+(' + evalNum(button.parent.parent.parent.get('x', '0')) + ')'
                        group_y = group_y + '+(' + evalNum(button.parent.parent.parent.get('y', '0')) + ')'
                        group_visibility = group_visibility + '*(' + button.parent.parent.parent.get('visibility','1') + ')'

                        group_x = evalNum(group_x)
                        group_y = evalNum(group_y)

                        # 第四层 Group标签
                        if button.parent.parent.parent.parent.name == 'Group':
                            # print('Quaternary', '\n')
                            group_x = group_x + '+(' + evalNum(button.parent.parent.parent.parent.get('x', '0')) + ')'
                            group_y = group_y + '+(' + evalNum(button.parent.parent.parent.parent.get('y', '0')) + ')'
                            group_visibility = group_visibility + '*(' + button.parent.parent.parent.parent.get('visibility', '1') + ')'

                            group_x = evalNum(group_x)
                            group_y = evalNum(group_y)

                group_x = str(group_x).replace('+(0)', '')
                group_y = str(group_y).replace('+(0)', '')

                group_x = evalNum(group_x)
                group_y = evalNum(group_y)

                group_visibility = str(group_visibility).replace('(1)*', '').replace('*(1)', '')
                if '*(0)' in group_visibility:
                    group_visibility = "0"

                # Printer
                print('\tgroup_x: ', group_x)
                print('\tgroup_y: ', group_y)
                # print('group_visibility: ', group_visibility, '\n')

                button_str.append(button.contents)

                # 获取原Button标签 其他属性
                # button_name = button.get('name', '')
                button_w = button.get('w', '1')
                button_h = button.get('h', '1')
                # button_align = button.get('align', '')
                # button_alignV = button.get('alignV', '')
                # button_alignChildren = button.get('alignChildren', '')
                # button_interceptTouch = button.get('interceptTouch', '')
                # button_alpha = button.get('alpha', '')

                button['x'] = group_x
                button['y'] = group_y
                button['visibility'] = group_visibility

                # Printer
                print(f'\t<Button x="{group_x}" y="{group_y}" w="{button_w}" h="{button_h}" visibility="{group_visibility}" >')
                # print('button_name: ', button.get('name', ''))
                # print('button_w: ', button.get('w', '1'))
                # print('button_h: ', button.get('h', '1'))
                # print('button_align: ', button.get('align', ''))
                # print('button_alignV: ', button.get('alignV', ''))
                # print('button_alignChildren: ', button.get('alignChildren', ''))
                # print('button_interceptTouch: ', button.get('interceptTouch', ''))
                # print('button_alpha: ', button.get('alpha', ''), '\n')
                new_end_tag = soup.new_tag('End')
                soup.Lockscreen.append(new_end_tag)
                new_end_tag.insert_after(button)
                new_end_tag.decompose()

                # # 新建一个Button标签，放于最下方
                # new_button = soup.new_tag('Button', x=group_x, y=group_y, visibility=group_visibility)
                # for i in range(len(button_str)):
                #     new_button.contents = button_str[i]
                # # print(new_button.contents)
                #
                # if button_name:
                #     new_button['name'] = button_name
                # if button_w:
                #     new_button['w'] = button_w
                # if button_h:
                #     new_button['h'] = button_h
                # if button_align:
                #     new_button['align'] = button_align
                # if button_alignV:
                #     new_button['alignV'] = button_alignV
                # if button_alignChildren:
                #     new_button['alignChildren'] = button_alignChildren
                # if button_interceptTouch:
                #     new_button['interceptTouch'] = button_interceptTouch
                # if button_alpha:
                #     new_button['alpha'] = button_alpha
                #
                # # print(new_button)
                # soup.Lockscreen.append(new_button)
                # # print(new_button)
                # sys.exit(100)
        print('\t')

        # 移除空标签
        for empty_text in soup.find_all():
            if empty_text.get('text') == '':
                print(f"Empty: {empty_text}")
                empty_text.decompose()

        for empty_text_exp in soup.find_all():
            if empty_text_exp.get('textExp') == '':
                print(f"Empty: {empty_text_exp}")
                empty_text_exp.decompose()

        # # 遍历所有标签元素
        # for tag in soup.find_all():
        #     # 检查属性是否有空值
        #     empty_attributes = [attr for attr, value in tag.attrs.items() if value == '']
        #
        #     # 如果有空属性，则打印相关信息
        #     if empty_attributes:
        #         # print(f'Empty: {tag.name}, Empty Attributes: {empty_attributes}')
        #         print(f'Empty: {tag}')

        for empty_tags in soup.find_all():
            empty_arr = list(set(empty_tags.contents))
            if len(empty_arr) == 1 and empty_arr[0] == '\n':
                print("👌Empty: {}".format(str(empty_tags).replace('\n', '')))
                empty_tags.decompose()

        print('\t')

    # 将修改后的xml字符串写入文件
    with open(manifest_xml, 'w', encoding='utf-8') as f:
        # f.write(str(soup.prettify(indent_width=4).replace('    ','\t')).replace('Lockscreen', manifest_root).replace('amp;gt;','gt;').replace('amp;lt;','lt;').replace('&amp;','&'))
        f.write(str(soup.prettify(indent_width=4).replace('    ', '\t')).replace('Lockscreen', manifest_root).replace(
            'amp;gt;', 'gt;').replace('amp;lt;', 'lt;').replace('amp;amp;', 'amp;'))


def intentMarket(save_file):

    # 代码后期功能补充
    with open(save_file, 'r', encoding='utf-8') as f:
        xml_str = f.read()
    soup = BeautifulSoup(xml_str, features="lxml-xml")

    # 针对 MIUI 第三方APP自动跳转商店
    if 'content://keyguard.notification/notifications' in str(soup) and '_pauseIntent="1"' not in str(soup):
        print('IntentMarket: 1')
        IntentCommand = 0
        for i in soup.find_all('IntentCommand'):
            IntentCommand += 1
            # 第三方APP自动跳转商店
            if not str(i.get('package')).startswith('com.android') \
                    and not str(i.get('package')).startswith('com.huawei') \
                    and not str(i.get('package')).startswith('com.example.android.notepad') \
                    and str(i.get('action')).upper() == 'ANDROID.INTENT.ACTION.MAIN'\
                    and i.get('package') is not None\
                    and i.get('class') is not None:
                hex_name = hex(zlib.crc32(str(i.get('class')).encode('UTF-8')))[2:].capitalize()
                img_var_name = f"{hex_name}_app"
                pkg_var_name = f"{hex_name}_app_pkg"
                pkg_var_exp = str(i.get('package'))
                cls_var_name = f"{hex_name}_app_cls"
                cls_var_exp = str(i.get('class'))
                print(
                    f"\t<IntentCommand action=\"{i.get('action')}\" package=\"{pkg_var_exp}\" class=\"{cls_var_exp}\" />")

                img_icon = f'&#60;Image name="{img_var_name}" w="1" h="1" srcType="ApplicationIcon" srcExp="@{pkg_var_name}" /&#62;'
                img_pkg_var = f'&#60;Var name="{pkg_var_name}" expression="\'{pkg_var_exp}\'" type="string" /&#62;'
                img_cls_var = f'&#60;Var name="{cls_var_name}" expression="\'{cls_var_exp}\'" type="string" /&#62;'
                soup.Lockscreen.Var.insert_before(f"{img_icon}\n{img_pkg_var}\n{img_cls_var}")

                origin_condition = str(i.get('condition')) if i.get('condition') is not None else '1'
                multi_command = f'&#60;MultiCommand condition="{origin_condition}" &#62;\n&#60;IntentCommand ' \
                                f'action="android.intent.action.VIEW" uriExp="\'market://details?id=' \
                                f'\'+@{pkg_var_name}+\'&amp;ref=mithemelocksreen\'" flags="268435456" condition="!#' \
                                f'{img_var_name}.bmp_width" /&#62;\n&#60;IntentCommand action="android.intent.action.MAIN" ' \
                                f'packageExp="@{pkg_var_name}" classExp="@{cls_var_name}" condition="#' \
                                f'{img_var_name}.bmp_width" /&#62;\n&#60;/MultiCommand&#62;'
                i.insert_after(multi_command)
                i.decompose()
        print('\t')

    # 针对 OPPO 组件卡加入 market="true"
    market_mode = 1
    # for tags in soup.find_all(True):
    #     if tags.name == 'Widget' and tags.get('version') == '10000':
    #         market_mode = 1
    #         print(f'MarketMode: {market_mode}')
    # if market_mode:
    #     for intent in soup.find_all('IntentCommand'):
    #         # print(intent)
    #         if intent.get('uri') != '@uri_theme' \
    #                 and 'com.android' not in str(intent) \
    #                 and 'com.coloros' not in str(intent) \
    #                 and 'com.oppo' not in str(intent) \
    #                 and 'com.nearme' not in str(intent) \
    #                 and 'com.heytap' not in str(intent):
    #             intent['market'] = 'true'
    #             print(intent)
    print(f'MarketMode: {market_mode}')
    if market_mode:
        for intent in soup.find_all('IntentCommand'):
            # 如果 uri 不等于 '@uri_theme' 并且不包含指定字符串，则设置 market 为 'true'
            # 新增 package 必须有值
            if intent.get('uri') != '@uri_theme' and intent.get('package') is not None and not any(
                    substring in str(intent)
                    for substring in ['com.android', 'com.coloros', 'com.oppo', 'com.nearme', 'com.heytap', 'com.oplus',
                                      'com.miui', 'com.vivo', 'com.bbk', 'com.iqoo', 'com.huawei', 'com.hihonor']
            ):
                intent['market'] = '1'
                # intent['market'] = 'true'
                print(f"\t{intent}")
    print('\t')

    # 针对 华为 图片缩放处理
    scale_type_mode = 1
    if scale_type_mode:
        print('ScaleType:')
        for image in soup.find_all('Image'):
            if '#' in str(image.get('w')) or '#' in str(image.get('h'))\
                    or '@' in str(image.get('w')) or '@' in str(image.get('w')):
                image['isBackground'] = 'false'
                image['scaleType'] = 'fill'
                print(f'\t{image}')
        print('\t')

    # 针对 vivo IntentCommand中加入category
    if soup.Widget:
        if soup.Widget.FramerateController:
            intent_category_mode = 0
        else:
            intent_category_mode = 1
    else:
        intent_category_mode = 1
    if intent_category_mode:
        print('Category:')
        for intent in soup.find_all('IntentCommand'):
            if str(intent.get('action')).upper() == 'ANDROID.INTENT.ACTION.MAIN'\
                    and intent.get('category') is None\
                    and intent.get('uri') is None\
                    and intent.get('uriExp') is None:
                intent['category'] = 'android.intent.category.LAUNCHER'
                print(f'\t{intent}')
        print('\t')

    # 针对 VariableAnimation.AniFrame / Item 中的 time 属性进行 abs(int(eval())) 操作
    # mResumeSpeed 预操作
    resume_speed = 1
    resume_speed_var = 'mResumeSpeed'
    for variable in soup.find_all('Var'):
        if variable.get('name') == resume_speed_var and variable.get('expression') is not None:
            resume_speed = str(variable['expression'])
            # print(resume_speed)
            resume_speed = eval(resume_speed)
            # resume_speed = max(eval(resume_speed), 1)
    # print(resume_speed)

    print('AniFrame:')
    for ani_frame in soup.find_all('AniFrame'):
        ani_frame['time'] = str(ani_frame.get('time')).replace(f'#{resume_speed_var}', str(resume_speed))
        if ani_frame.get('time') and ani_frame.parent.name == 'VariableAnimation'\
                and any(op in ani_frame.get('time') for op in "+-*/")\
                and all(forbidden_char not in ani_frame.get('time') for forbidden_char in "#@"):
            ani_frame['time'] = abs(int(eval(str(ani_frame.get('time')))))
            print(f"\t{ani_frame.parent.parent.get('name')}: {ani_frame}")
    print('\t')

    for ani_item in soup.find_all('Item'):
        if ani_item.parent.name == 'VariableAnimation':
            ani_item['time'] = str(ani_item.get('time')).replace(f'#{resume_speed_var}', str(resume_speed))
            if ani_item.get('time')\
                    and any(op in ani_item.get('time') for op in "+-*/")\
                    and all(forbidden_char not in ani_item.get('time') for forbidden_char in "#@"):
                ani_item['time'] = abs(int(eval(str(ani_item.get('time')))))
                # print(f"\t{ani_item.parent.parent.get('name')}: {ani_item}")

    # 带动画的 Image 标签加入 name 属性
    print('Image: ')
    for image in soup.find_all('Image'):
        if image.get('name') is None:
            time_sys = str(time.time())
            # print(time_sys)
            image_uuid = image.encode('UTF-8')
            image_uuid2 = hex(zlib.crc32(time_sys.encode('UTF-8')))[2:].capitalize()
            image_name = hex(zlib.crc32(image_uuid))[2:].capitalize() + image_uuid2

            for child_tag in image.find_all(recursive=False):
                if 'Animation' in str(child_tag.name):
                    image['name'] = image_name
                    print(f"\t{str(child_tag.name)}: <Image name=\"{image_name}\" src=\"{image.get('src')}\" >")
    print('\t')

    # 没有 name 属性的 threshold 标签加入 name 属性
    print('Var.threshold: ')
    for var_thrs in soup.find_all('Var'):
        if var_thrs.get('threshold') == '1' and var_thrs.get('name') is None:
            time_sys = str(time.time())
            # print(time_sys)
            var_thrs_uuid = var_thrs.encode('UTF-8')
            var_thrs_uuid2 = hex(zlib.crc32(time_sys.encode('UTF-8')))[2:].capitalize()
            var_thrs_name = hex(zlib.crc32(var_thrs_uuid))[2:].capitalize() + var_thrs_uuid2

            for child_tag in var_thrs.find_all(recursive=False):
                if 'Trigger' in str(child_tag.name):
                    var_thrs['name'] = var_thrs_name
                    print(
                        f"\t{str(child_tag.name)}: <Var name=\"{var_thrs_name}\" expression=\"{var_thrs.get('expression')}\" threshold=\"1\" >")
    print('\t')

    # 去除小部件下无用的Function
    langs_id = 4
    if langs_id == 4:
        # 查询所有 FunctionCommand 标签的 name 属性值，并存储到数组中
        function_command_names = [command['target'] for command in soup.find_all('FunctionCommand')]
        if len(function_command_names):
            print(f'Function: {function_command_names}')
        # 查询所有 Function 标签
        functions = soup.find_all('Function')

        # 遍历 Function 标签并检查 name 属性是否在数组中，如果不在则删除该标签
        for function in functions:
            if function['name'] not in function_command_names:
                function.decompose()  # 删除该标签

    # 去除无用的VarArray
    var_array = 1
    if var_array == 1:
        print('VarArray:')
        for var_arr in soup.find_all('Var'):
            if var_arr.parent.name == 'Vars':
                if var_arr.parent.parent.get('type') == 'string':
                    var_arr_type = '@'
                else:
                    var_arr_type = '#'
                var_arr_name = str(var_arr_type + str(var_arr['name']))
                # {var_arr.parent.parent.name}:
                if var_arr_name not in str(soup):
                    print(f"\t{var_arr_name}")
                    var_arr.parent.parent.decompose()
        print('\t')

    with open(save_file, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify(indent_width=4).replace('    ', '\t').
                    replace('&amp;#60;', '<').replace('&amp;#62;', '>').replace('&amp;#', '&#')))
