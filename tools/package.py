import os
import pyperclip

clipboard_content = pyperclip.paste().replace('\\', '/').replace('"', '')

# 判断剪贴板内容是否为文件夹
if os.path.isdir(clipboard_content):
    # 提取最后一部分作为文件夹名称
    target_folder_name = os.path.join('', clipboard_content)
else:
    # 获取上一级文件夹路径并提取最后一部分作为文件夹名称
    target_folder_name = os.path.join('', os.path.dirname(clipboard_content))

print('\t')
print(f'Source: {target_folder_name}\n')

