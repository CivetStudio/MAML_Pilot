import os
import sys
import pyperclip
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

#
# maml_main_xml = os.path.dirname(pyperclip.paste().replace('\\', '/').replace('"', ''))
# maml_file_name = os.path.basename(maml_main_xml)

maml_main_xml = pyperclip.paste().replace('\\', '/').replace('"', '')
maml_rule_file = "maml.xml"
maml_file_name = os.path.basename(maml_main_xml)

# 判断 maml_file_name 是否以 maml_rule_file 结尾
if maml_rule_file not in maml_file_name:
    print(f"Error: File must be '{maml_rule_file}'")
    sys.exit(1)

print('\t')
execute_times = 0
current_script_path = os.path.abspath(__file__)
parent_folder_path = os.path.dirname(current_script_path)
# main_script_path = os.path.join(parent_folder_path, 'main.py')
main_script_path = os.path.join(parent_folder_path, 'main.py')
print(f'Source: {maml_main_xml}')
print(f'Script: {main_script_path}\n')


def get_logging_time():
    # 获取当前时间
    current_time = datetime.now()
    # 格式化输出
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

    return formatted_time


def execute_script():

    global execute_times
    execute_times += 1

    pyperclip.copy(file_to_monitor)
    script_path = main_script_path  # 替换为你的 Python 脚本文件路径
    try:
        # 使用 print 输出
        # print(f"Start: {get_logging_time()}"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        result = subprocess.run(['python3', script_path], check=True)
        print(f"{execute_times} | {get_logging_time()}: {result}")
        print('\t')

        # 处理 result 中的输出信息
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}.")
        # 处理非零返回状态的情况

    def show_notification(title, text):
        applescript = f'display notification "{text}" with title "{title}"'
        subprocess.run(["osascript", "-e", applescript])

    # 示例调用
    show_notification("maml.xml", "代码更新成功")


class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        print(f'Event type: {event.event_type}, Path: {event.src_path}')

        # 在这里调用你的代码，例如执行你的文件
        execute_your_code()


def execute_your_code():
    # 在这里执行你的代码，例如运行文件或调用其他函数
    # print(f'Executing your code for file: {file_path}')
    execute_script()


def monitor_folder(folder_path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# 使用示例
file_to_monitor = maml_main_xml  # 监听对象
monitor_folder(file_to_monitor)
