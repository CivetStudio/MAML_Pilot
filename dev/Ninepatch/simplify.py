import subprocess

import pyperclip

input_path = './test/myninepatch.9.png'
output_path = './test/myninepatch2.9.png'

if pyperclip.paste():
    input_path = output_path = pyperclip.paste()

aapt_command = f'./aapt s -i {input_path} -o {output_path}'
result = subprocess.run(aapt_command, shell=True, capture_output=True, text=True)
print(result.stdout)
