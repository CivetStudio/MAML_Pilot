import pyperclip
from PIL import Image
import os
import os.path
import re
import subprocess

preview_url = pyperclip.paste().split('\n')
print(f'preview_url: {preview_url}')


def main():
    script_path = 'main.py'  # 替换为你的 Python 脚本文件路径
    try:
        # 使用 print 输出
        # stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        result = subprocess.run(['python3', script_path], check=True)
        print('\t')

        # 处理 result 中的输出信息
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}.")
        # 处理非零返回状态的情况


for k in range(len(preview_url)):
    pyperclip.copy(preview_url[k])
    print(preview_url[k])
    main()
