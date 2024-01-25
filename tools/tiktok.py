import subprocess
import time
import random


def click_screen(x, y):
    devices_command = f"adb shell input tap {x} {y}"
    result = subprocess.run(devices_command, shell=True, capture_output=True, text=True)
    print(result)
    # adb_shell(f"input tap {x} {y}")


def main():
    # 循环点击屏幕
    for _ in range(50):  # 点击10次，可以根据需要调整
        # 生成随机坐标（示例范围，根据实际屏幕分辨率调整）
        target_x = random.randint(100, 980)
        target_y = random.randint(328, 1238)

        click_screen(target_x, target_y)
    time.sleep(random.randint(1, 5))  # 间隔2秒再次点击，可以根据需要调整
    main()


if __name__ == "__main__":
    main()