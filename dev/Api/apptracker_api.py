import pyperclip
import requests
import random


def generate_random_ip():
    # 生成随机的 IPv4 地址
    random_ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    print(random_ip)
    return random_ip


def generate_random_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/56.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/16.16299",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    ]
    accept_languages = [
        "en-US,en;q=0.5",
        "en-GB,en;q=0.5",
        "fr-FR,fr;q=0.5",
        "de-DE,de;q=0.5",
        "es-ES,es;q=0.5",
    ]

    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": random.choice(accept_languages),
        "X-Forwarded-For": generate_random_ip(),  # 添加随机 IP 地址
    }

    return headers


def fetch_app_info(input_query):
    url = f"https://apptracker-api.cn2.tiers.top/api/appInfo?q={input_query}&page=1"
    headers = generate_random_headers()

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Response JSON:", response.json())
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}, Response: {response.text}")


if __name__ == "__main__":
    input_query = input("输入APP名称 (如QQ音乐)：")  # 替换为实际查询参数
    if input_query:
        result = fetch_app_info(input_query)
        if result['items']:
            max_count_item = max(result['items'], key=lambda x: x['count'])
            print("Count JSON:", max_count_item)
            intent_tag = 'IntentCommand'
            intent_action = 'android.intent.action.MAIN'
            intent_package = max_count_item['packageName']
            intent_class = max_count_item['activityName']
            intent_command = f'<{intent_tag} action="{intent_action}" package="{intent_package}" class="{intent_class}" />'
            print("Tags:", intent_command)
            pyperclip.copy(intent_command)
            print('\n',result)
    else:
        print("请输入正确的APP名称！")
