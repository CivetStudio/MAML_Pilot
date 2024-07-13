import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import subprocess
from subprocess import Popen, PIPE

dev_path = '/Users/wangshilong/Desktop/导出/MAMLPilot'
if dev_path not in sys.path:
    sys.path.append(dev_path)


def main(quit_todesk=0):
    global connect_time

    # 创建浏览器实例
    driver = webdriver.Firefox()

    # 打开登录页面
    driver.get('http://192.168.0.1/noAuth/user_auth.html')

    # 查找用户名和密码输入框，并输入相应内容
    username_input = driver.find_element(By.NAME, 'userName')
    password_input = driver.find_element(By.NAME, 'userPasswd')

    username_input.send_keys('vgoing')
    password_input.send_keys('1122334455')

    # 点击登录按钮
    login_btn = driver.find_element(By.ID, 'login_btn')
    login_btn.click()

    time.sleep(1)

    # 在关闭浏览器之前获取页面内容
    page_content = driver.page_source
    print("当前页面内容：", page_content)
    if '认证成功' in page_content:
        if connect_time == 0:
            show_notification(get_wifi_ssid(), "Wi-Fi 认证成功")
        connect_time += 1
        if 'PYCHARM_HOSTED' in os.environ:
            from dev.Refactor.functions import formatDate
            _f = formatDate('yyyy-MM-dd HH:mm:ss', time.time() * 1000)
            print('认证成功', _f)
        else:
            pass
        # print('认证成功', formatDate('yyyy-MM-dd HH:mm:ss', time.time() * 1000))
        # 关闭浏览器
        driver.quit()

        if quit_todesk:
            # 密码
            sudo_password = "997975"

            # 创建一个子进程，并与其进行交互
            process = Popen(['sudo', '-S', 'pkill', '-f', 'ToDesk'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)

            # 向子进程发送密码
            process.stdin.write(sudo_password + '\n')
            process.stdin.flush()

            # 获取输出
            output, err = process.communicate()

            # 打印输出
            # print("输出：", output)
            # print("错误：", err)

            time.sleep(2)

            # 打开应用程序
            subprocess.call(["open", "-n", "/Applications/ToDesk.app"])

        time.sleep(1500)
        main()
    else:
        main()


if __name__ == '__main__':
    def get_wifi_ssid():
        import platform
        try:
            os_name = platform.system()
            if os_name == "Windows":
                wifi_result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
                output = wifi_result.stdout.strip().split("\n")
                ssid_name = [line.split(":")[1].strip() for line in output if "SSID" in line][0]
                return ssid_name
            elif os_name == "Darwin":  # macOS
                wifi_result = subprocess.run(["/usr/sbin/networksetup", "-getairportnetwork", "en0"],
                                             capture_output=True,
                                             text=True)
                output = wifi_result.stdout.strip()
                ssid_name = output.split(":")[1].strip()
                return ssid_name
            else:
                print("Unsupported operating system.")
                return None
        except Exception as wifi_e:
            print(f"Wi-Fi Error: {wifi_e}")


    def show_notification(title, text):
        applescript = f'display notification "{text}" with title "{title}"'
        subprocess.run(["osascript", "-e", applescript])

    wifi_ssid = get_wifi_ssid()
    wifi_in_vgoing = get_wifi_ssid() == "vgoing"

    if wifi_in_vgoing:
        connect_time = 0
        main()
    else:
        show_notification(get_wifi_ssid(), "Wi-Fi is not 'vgoing'")
        sys.exit(0)

