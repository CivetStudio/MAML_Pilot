# Todo List
# 2024/02/03 - 全平台锁屏打包工具（支付华为/OPPO/VIVO/荣耀）
# 2024/04/07 - 新增 MIUI 平台打包支持（isnull转换，屏蔽充电动画）

import os
import sys
import time
import shutil
import zipfile
from PIL import Image
import pyperclip


def create_blank_image(width, height, color=(255, 255, 255)):
    return Image.new("RGB", (width, height), color)


def save_images(image_name):
    image = create_blank_image(1080, 1920, color=(255, 255, 255))
    # 保存图片
    image.save(image_name, dpi=(72, 72))


def replace_in_text_file(txt_path, old_str, new_str):
    try:
        with open(txt_path, 'r') as file:
            content = file.read()

        # 进行替换操作
        new_content = content.replace(old_str, new_str)

        with open(txt_path, 'w') as file:
            file.write(new_content)

        # print(f"Successfully replaced in {txt_path}")
    except Exception as txt_e:
        print(f"Error replacing in {txt_path}: {txt_e}")


def clean_cache(folder_path):
    for _root, _, _files in os.walk(folder_path):
        for filename in _files:
            _file_path = os.path.join(_root, filename)
            if filename.startswith("._") or filename == ".DS_Store":
                try:
                    os.remove(_file_path)
                    # print(f'Remove: {filename}')
                except Exception as _file_e:
                    print(f"Exception: {_file_e}")


def zip_folder(folder_path, zip_path):
    # os.path.basename(root) == 'lockscreen' or os.path.basename(root) == 'advance'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if any(item == file for item in forbid_items):
                    file_path = os.path.join(root, file)
                    print('\t', file_path, 'Removed👌')
                else:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname=arcname)


def copy_folder_contents(source_folder, destination_folder):
    try:
        # 遍历源文件夹内的所有内容（包括子文件夹和子文件）
        for root, dirs, files in os.walk(source_folder):
            for file_name in files:
                source_file_path = os.path.join(root, file_name)
                # 获取相对路径，用于构建目标文件夹中的路径
                relative_path = os.path.relpath(source_file_path, source_folder)
                destination_file_path = os.path.join(destination_folder, relative_path)
                # 确保目标文件夹中的路径存在
                os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
                shutil.copy2(source_file_path, destination_file_path)

        # print(
        #     f"Contents of folder '{source_folder}' (including subfolders) copied to '{destination_folder}' successfully.")
    except FileNotFoundError:
        print(f"Source folder '{source_folder}' not found.")
    except PermissionError:
        print(f"Permission error. Unable to copy folder contents.")


lock_path = '/theme/lock'
temp_folder = 'temp_folder'
tmp_huawei = temp_folder + '_' + 'huawei'
tmp_honor = temp_folder + '_' + 'honor'
tmp_oppo = temp_folder + '_' + 'oppo'
tmp_vivo = temp_folder + '_' + 'vivo'
tmp_xiaomi = temp_folder + '_' + 'xiaomi'
async_load = 'false'

hw_theme_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<HWTheme>
  <item style="slide"/>
  <item package="com.huawei.ucdlockscreen"/>
  <item dynamicPath="lockscreen"/>
  <item minversion="2.0.24"/>
  <item title-cn="华为官方主题"/>
  <item title="Huawei Themes"/>
  <item maxHeight="2160"/>
  <item engineType="HWThemeEngine"/>
  <item baseVersion="6.0"/>
  <item asyncLoad="{async_load}" />
</HWTheme>
"""

ho_theme_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<HnTheme>
  <item style="slide"/>
  <item package="com.hihonor.android.thememanager"/>
  <item dynamicPath="lockscreen"/>
  <item minversion="2.0.24"/>
  <item title-cn="华为官方主题"/>
  <item title="Huawei Themes"/>
  <item maxHeight="2160"/>
  <item baseVersion="6.0"/>
  <item engineType="HWThemeEngine"/>
</HnTheme>
"""

time_sys = int(time.time() * 1000)
vivo_author = '灵貓'
print(f'Start: {time_sys}')
vivo_theme_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<theme>
    <id>{time_sys}</id>
    <version><![CDATA[3.0.0]]></version>
    <titles>
        <title locale="zh_CN"><![CDATA[{time_sys}]]></title>
    </titles>
    <authors>
        <author locale="zh_CN"><![CDATA[{vivo_author}]]></author>
    </authors>
    <designers>
        <designer locale="zh_CN"><![CDATA[-12]]></designer>
    </designers>
    <descriptions>
        <description local="zh_CN" locale="zh_CN"></description>
    </descriptions>
</theme>
"""


def pack_huawei(path, filename="HUAWEI"):
    global huawei_zip_path

    if os.path.exists(tmp_huawei):
        shutil.rmtree(tmp_huawei)

    os.mkdir(tmp_huawei)
    tmp_huawei_0 = os.path.join(os.path.abspath(tmp_huawei), 'unlock')
    os.mkdir(tmp_huawei_0)
    tmp_huawei_1 = os.path.join(os.path.abspath(tmp_huawei_0), 'lockscreen')
    os.mkdir(tmp_huawei_1)
    # 将XML内容写入xml文件
    with open(os.path.join(os.path.abspath(tmp_huawei_0), 'theme.xml'), "w") as xml_file:
        xml_file.write(hw_theme_xml)
    copy_folder_contents(path, tmp_huawei_1)

    huawei_path = os.path.abspath(tmp_huawei).replace(tmp_huawei, 'HUAWEI')
    huawei_zip_path = os.path.join(os.path.dirname(path), f'{theme_name}_{filename}.zip')

    shutil.move(tmp_huawei, huawei_path)
    clean_cache(huawei_path)
    platform_id = None
    update_array(platform_id)
    zip_folder(huawei_path, huawei_zip_path)

    if os.path.exists(tmp_huawei):
        shutil.rmtree(tmp_huawei)

    if os.path.exists(huawei_path):
        shutil.rmtree(huawei_path)


def process_xml(honor_xml_file):
    from tools.honor import detect_lockscreen_view, process_lockscreen_var
    detect_lockscreen_view(honor_xml_file)
    process_lockscreen_var(honor_xml_file)


def pack_honor(path, filename="HONOR"):
    global honor_zip_path

    if os.path.exists(tmp_honor):
        shutil.rmtree(tmp_honor)

    os.mkdir(tmp_honor)
    tmp_honor_0 = os.path.join(os.path.abspath(tmp_honor), 'unlock')
    os.mkdir(tmp_honor_0)
    tmp_honor_1 = os.path.join(os.path.abspath(tmp_honor_0), 'lockscreen')
    os.mkdir(tmp_honor_1)
    # 将XML内容写入xml文件
    with open(os.path.join(os.path.abspath(tmp_honor_0), 'theme.xml'), "w") as xml_file:
        xml_file.write(ho_theme_xml)
    copy_folder_contents(path, tmp_honor_1)

    process_xml_honor = 1
    if process_xml_honor:
        process_xml(os.path.join(tmp_honor_1, 'manifest.xml'))

    honor_path = os.path.abspath(tmp_honor).replace(tmp_honor, 'honor')
    honor_zip_path = os.path.join(os.path.dirname(path), f'{theme_name}_{filename}.zip')

    shutil.move(tmp_honor, honor_path)
    clean_cache(honor_path)
    platform_id = None
    update_array(platform_id)
    zip_folder(honor_path, honor_zip_path)

    if os.path.exists(tmp_honor):
        shutil.rmtree(tmp_honor)

    if os.path.exists(honor_path):
        shutil.rmtree(honor_path)


def pack_oppo(path, filename="OPPO"):
    global oppo_zip_path

    if os.path.exists(tmp_oppo):
        shutil.rmtree(tmp_oppo)

    os.mkdir(tmp_oppo)
    tmp_oppo_0 = os.path.join(os.path.abspath(tmp_oppo), 'lockscreen')
    os.mkdir(tmp_oppo_0)
    tmp_oppo_1 = os.path.join(os.path.abspath(tmp_oppo_0), 'advance')
    os.mkdir(tmp_oppo_1)
    copy_folder_contents(path, tmp_oppo_1)

    xml_path = os.path.join(tmp_oppo_1, 'manifest.xml')
    replace_in_text_file(xml_path, ' _const', ' const')
    replace_in_text_file(xml_path, 'globalPersist', '_glb')

    oppo_folder = ['2x1', '7x3', '11x5', '13x6', '19x9', '20x9', '67x30', '301x135', '403x180', '693x310']
    for f in range(len(oppo_folder)):
        oppo_folder_path = os.path.join(tmp_oppo_1, oppo_folder[f])
        oppo_xml_folder = os.path.exists(oppo_folder_path)
        xml_folder_path = os.path.join(oppo_folder_path, 'manifest.xml')
        if not oppo_xml_folder:
            os.mkdir(oppo_folder_path)
            shutil.copy2(xml_path, xml_folder_path)

    oppo_path = os.path.abspath(tmp_oppo).replace(tmp_oppo, 'OPPO')

    oppo_lockstyle_path = os.path.join(tmp_oppo, 'lockstyle.zip')
    oppo_lockstyle_path_f = os.path.join(tmp_oppo, 'lockstyle')

    clean_cache(tmp_oppo_1)
    platform_id = 'oppo'
    update_array(platform_id)
    zip_folder(tmp_oppo_0, oppo_lockstyle_path)
    shutil.move(oppo_lockstyle_path, oppo_lockstyle_path_f)
    shutil.rmtree(tmp_oppo_1)
    shutil.move(oppo_lockstyle_path_f, os.path.join(tmp_oppo_0, 'lockstyle'))

    oppo_zip_path = os.path.join(os.path.dirname(path), f'{theme_name}_{filename}.zip')

    zip_folder(tmp_oppo, oppo_zip_path)

    if os.path.exists(tmp_oppo):
        shutil.rmtree(tmp_oppo)

    if os.path.exists(oppo_path):
        shutil.rmtree(oppo_path)


def pack_vivo(path, filename="VIVO"):
    global vivo_zip_path

    if os.path.exists(tmp_vivo):
        shutil.rmtree(tmp_vivo)

    os.mkdir(tmp_vivo)
    tmp_vivo_0 = os.path.join(os.path.abspath(tmp_vivo), 'lockscreen')
    os.mkdir(tmp_vivo_0)
    tmp_vivo_1 = os.path.join(os.path.abspath(tmp_vivo_0), 'lockscreen')
    os.mkdir(tmp_vivo_1)
    tmp_vivo_2 = os.path.join(os.path.abspath(tmp_vivo_0), 'preview')
    os.mkdir(tmp_vivo_2)

    # preview: preview_lockscreen_0.jpg, preview_lockscreen_1.jpg
    preview_images = ['preview_lockscreen_0.jpg', 'preview_lockscreen_1.jpg']
    for image in range(len(preview_images)):
        preview_image_path = os.path.join(tmp_vivo_2, str(preview_images[image]))
        save_images(preview_image_path)

    # 将XML内容写入xml文件
    with open(os.path.join(os.path.abspath(tmp_vivo_0), 'description.xml'), "w") as xml_file:
        xml_file.write(vivo_theme_xml)
    copy_folder_contents(path, tmp_vivo_1)

    xml_path = os.path.join(tmp_vivo_1, 'manifest.xml')
    replace_in_text_file(xml_path, ',5,0)', ',5,5)')
    replace_in_text_file(xml_path, 'globalPersist', '_glb')
    replace_in_text_file(xml_path, '_const="true"', '')

    vivo_lockscreen_path = os.path.join(os.path.dirname(tmp_vivo_1), f'{time_sys}.zip')
    clean_cache(tmp_vivo_1)
    platform_id = None
    update_array(platform_id)
    zip_folder(tmp_vivo_1, vivo_lockscreen_path)
    shutil.rmtree(tmp_vivo_1)
    os.mkdir(tmp_vivo_1)
    shutil.move(vivo_lockscreen_path, tmp_vivo_1)

    vivo_lockzip_path = os.path.join(os.path.dirname(tmp_vivo_0), 'lockscreen.zip')
    vivo_lockitz_path = vivo_lockzip_path.replace('lockscreen.zip', 'lockscreen.itz')
    zip_folder(tmp_vivo_0, vivo_lockzip_path)
    shutil.move(vivo_lockzip_path, vivo_lockitz_path)
    shutil.rmtree(tmp_vivo_0)

    vivo_path = os.path.abspath(tmp_vivo).replace(tmp_vivo, 'VIVO')
    vivo_zip_path = os.path.join(os.path.dirname(path), f'{theme_name}_{filename}.zip')

    shutil.move(tmp_vivo, vivo_path)
    clean_cache(vivo_path)
    zip_folder(vivo_path, vivo_zip_path)

    if os.path.exists(tmp_vivo):
        shutil.rmtree(tmp_vivo)

    if os.path.exists(vivo_path):
        shutil.rmtree(vivo_path)


def pack_xiaomi(path, filename="XIAOMI"):
    global xiaomi_zip_path

    if os.path.exists(tmp_xiaomi):
        shutil.rmtree(tmp_xiaomi)

    os.mkdir(tmp_xiaomi)
    tmp_xiaomi_0 = os.path.join(os.path.abspath(tmp_xiaomi), 'lockscreen')
    os.mkdir(tmp_xiaomi_0)
    tmp_xiaomi_1 = os.path.join(os.path.abspath(tmp_xiaomi_0), 'advance')
    os.mkdir(tmp_xiaomi_1)

    copy_folder_contents(path, tmp_xiaomi_1)

    from tools.xiaomi import process_xml_xiaomi
    process_xml_xiaomi(os.path.join(tmp_xiaomi_1, 'manifest.xml'))

    xiaomi_path = os.path.abspath(tmp_xiaomi).replace(tmp_xiaomi, 'XIAOMI')
    xiaomi_zip_path = os.path.join(os.path.dirname(path), f'{theme_name}_{filename}.zip')

    shutil.move(tmp_xiaomi, xiaomi_path)
    clean_cache(xiaomi_path)
    platform_id = 'xiaomi'
    update_array(platform_id)
    zip_folder(xiaomi_path, xiaomi_zip_path)

    if os.path.exists(tmp_xiaomi):
        shutil.rmtree(tmp_xiaomi)

    if os.path.exists(xiaomi_path):
        shutil.rmtree(xiaomi_path)


def pack_simple(path, filename=None):
    tmp_simple = eval(f'tmp_{filename.lower()}')

    if os.path.exists(tmp_simple):
        shutil.rmtree(tmp_simple)

    tmp_simple_1 = tmp_simple

    copy_folder_contents(path, tmp_simple_1)

    if filename == 'HUAWEI':
        platform_id = None
        pass

    if filename == 'HONOR':
        tmp_honor_1 = tmp_simple_1
        process_xml_honor = 1
        if process_xml_honor:
            process_xml(os.path.join(tmp_honor_1, 'manifest.xml'))
        platform_id = None

    if filename == 'OPPO':
        tmp_oppo_1 = tmp_simple_1
        xml_path = os.path.join(tmp_oppo_1, 'manifest.xml')
        replace_in_text_file(xml_path, ' _const', ' const')
        replace_in_text_file(xml_path, 'globalPersist', '_glb')

        oppo_folder = ['2x1', '7x3', '11x5', '13x6', '19x9', '20x9', '67x30', '301x135', '403x180', '693x310']
        for f in range(len(oppo_folder)):
            oppo_folder_path = os.path.join(tmp_oppo_1, oppo_folder[f])
            oppo_xml_folder = os.path.exists(oppo_folder_path)
            xml_folder_path = os.path.join(oppo_folder_path, 'manifest.xml')
            if not oppo_xml_folder:
                os.mkdir(oppo_folder_path)
                shutil.copy2(xml_path, xml_folder_path)
        platform_id = 'oppo'

    if filename == 'VIVO':
        tmp_vivo_1 = tmp_simple_1
        xml_path = os.path.join(tmp_vivo_1, 'manifest.xml')
        replace_in_text_file(xml_path, ',5,0)', ',5,5)')
        replace_in_text_file(xml_path, 'globalPersist', '_glb')
        replace_in_text_file(xml_path, '_const="true"', '')
        platform_id = None

    if filename == 'XIAOMI':
        from tools.xiaomi import process_xml_xiaomi
        process_xml_xiaomi(os.path.join(tmp_simple_1, 'manifest.xml'))
        platform_id = 'xiaomi'

    simple_path = os.path.abspath(tmp_simple).replace(tmp_simple, filename)
    simple_zip_path = os.path.join(os.path.dirname(path), f'{theme_name}_{filename}.zip')

    shutil.move(tmp_simple, simple_path)
    clean_cache(simple_path)
    update_array(platform_id)
    zip_folder(simple_path, simple_zip_path)

    if os.path.exists(tmp_simple):
        shutil.rmtree(tmp_simple)

    if os.path.exists(simple_path):
        shutil.rmtree(simple_path)

    global huawei_zip_path
    global oppo_zip_path
    global vivo_zip_path
    global honor_zip_path
    global xiaomi_zip_path

    if filename == 'HUAWEI':
        huawei_zip_path = simple_zip_path
    if filename == 'OPPO':
        oppo_zip_path = simple_zip_path
    if filename == 'VIVO':
        vivo_zip_path = simple_zip_path
    if filename == 'HONOR':
        honor_zip_path = simple_zip_path
    if filename == 'XIAOMI':
        xiaomi_zip_path = simple_zip_path


def main(platform=1, hw=0, oppo=0, vivo=0, honor=0, xiaomi=0):
    global theme_name

    target_pack_path = pyperclip.paste().split('\n')
    print(f'Source: {target_pack_path}')

    try:
        platform_all_e_honor = platform
        if platform_all_e_honor:
            platform_hw = 1
            platform_oppo = 1
            platform_vivo = 1
            platform_honor = 1
            platform_xiaomi = 1
        else:
            platform_hw = hw
            platform_oppo = oppo
            platform_vivo = vivo
            platform_honor = honor
            platform_xiaomi = xiaomi

        for k in range(len(target_pack_path)):
            if os.path.isdir(target_pack_path[k]):
                theme_name_list = target_pack_path[k].split('/')
                if theme_name_list[-1] == 'advance':
                    theme_name = theme_name_list[-5]
                    # print(theme_name)
                else:
                    theme_name = target_pack_path[-1]
                    # print(theme_name)
                if current_dir != os.path.dirname(target_pack_path[k]):
                    pass
                    # for i in range(len(theme_name)):
                    #     if str(theme_name[i]) == 'advance':
                    #         theme_name = theme_name[max(i - 4, 0)]
                else:
                    # print(current_dir, os.path.dirname(target_pack_path[k]))
                    sys.exit("Source Folder is 'Sample Folder'")
                    # theme_name = os.path.basename(target_pack_path[k])
                print(f'Theme: {theme_name}')
                if platform_hw:
                    print('Pack Huawei: \t')
                    if simple_mode:
                        pack_simple(target_pack_path[k], 'HUAWEI')
                    else:
                        pack_huawei(target_pack_path[k])
                    print('\t', huawei_zip_path)
                if platform_honor:
                    print('Pack Honor: \t')
                    if simple_mode:
                        pack_simple(target_pack_path[k], 'HONOR')
                    else:
                        pack_honor(target_pack_path[k])
                    print('\t', honor_zip_path)
                if platform_oppo:
                    print('Pack Oppo: \t')
                    if simple_mode:
                        pack_simple(target_pack_path[k], 'OPPO')
                    else:
                        pack_oppo(target_pack_path[k])
                    print('\t', oppo_zip_path)
                if platform_vivo:
                    print('Pack Vivo: \t')
                    if simple_mode:
                        pack_simple(target_pack_path[k], 'VIVO')
                    else:
                        pack_vivo(target_pack_path[k])
                    print('\t', vivo_zip_path)
                if platform_xiaomi:
                    print('Pack Xiaomi: \t')
                    if simple_mode:
                        pack_simple(target_pack_path[k], 'XIAOMI')
                    else:
                        pack_xiaomi(target_pack_path[k])
                    print('\t', xiaomi_zip_path)
                if platform_all_e_honor:
                    print('Merge All Platform: \t')
                    zip_path_list = [huawei_zip_path, oppo_zip_path, vivo_zip_path, honor_zip_path, xiaomi_zip_path]
                    # print(zip_path_list)
                    # 将三平台zip解压到对应文件夹后，重新打包
                    for z in range(len(zip_path_list)):
                        zip_list_folder = zip_path_list[z].replace('.zip', '').replace(f'{theme_name}_', '')
                        zip_list_folder = os.path.join(os.path.dirname(zip_list_folder), theme_name, os.path.basename(zip_list_folder))
                        # print(zip_list_folder)
                        with zipfile.ZipFile(zip_path_list[z], 'r') as zip_ref:
                            zip_ref.extractall(zip_list_folder)
                        os.remove(zip_path_list[z])

                    zip_folder_path = os.path.dirname(zip_list_folder)
                    zip_all_path = os.path.join(os.path.dirname(huawei_zip_path), f'{theme_name}.zip')
                    global forbid_items
                    forbid_items = []
                    zip_folder(zip_folder_path, zip_all_path)
                    shutil.rmtree(zip_folder_path)
                    print('\t', zip_all_path)
                print('Success🍺')
            else:
                print(f"Error: '{target_pack_path[k]}' is not a folder")
    except Exception as e:
        print(f"Error: {e}")


def update_array(platform_id):
    global forbid_items

    is_oversea_mode = 0
    if is_oversea_mode:
        forbid_items = ['maml.xml', 'source.xml', 'anti.xml', 'oversea.jpg', 'red.png']
    else:
        forbid_items = ['maml.xml', 'source.xml', 'anti.xml', 'red.png']
    forbid_items_add = []
    forbid_items_add2 = []

    if platform_id != 'oppo' or platform_id == 'xiaomi':
        forbid_items_add = ['bg.png', 'bs.jpg']
    if platform_id != 'xiaomi':
        forbid_items_add2 = ['close.png']
    if is_oversea_mode:
        forbid_items = forbid_items + forbid_items_add + forbid_items_add2
    else:
        forbid_items = forbid_items + forbid_items_add + forbid_items_add2


# 执行主程序
if __name__ == '__main__':
    simple_mode = 1
    # platform = 1, hw = 0, oppo = 0, vivo = 0, honor = 0, xiaomi = 1
    current_dir = os.path.dirname(sys.argv[0])
    main(1, 0, 0, 1, 0, 0)
