import pyperclip
import requests
import random
import json


def generate_random_ip():
    # 生成随机的 IPv4 地址
    random_ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    # print(random_ip)
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


def fetch_location_info(key='M4ABZ-3DRRU-O66VP-2CNPJ-HCKS5-6TBEV'):
    # url = 'https://api.map.baidu.com/location/ip?ak=jCTWzgCK1QcypTrgxosTChNO'
    # url = 'https://restapi.amap.com/v3/ip?key=0113a13c88697dcea6a445584d535837&ip={ip}'
    url = f"https://apis.map.qq.com/ws/location/v1/ip?key={key}"
    headers = generate_random_headers()

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # print("Response JSON:", response.json())
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}, Response: {response.text}")


def fetch_weather_info(latitude='', longitude='', appKey='weather20151024', sign='zUFJoAR2ZVrDy1vF3D07'):
    url = f"https://weatherapi.market.xiaomi.com/wtr-v3/weather/all?latitude={latitude}&longitude={longitude}&isLocated=true&days=15&appKey={appKey}&sign={sign}&romVersion=7.2.16&appVersion=87&alpha=false&isGlobal=false&device=cancro&modDevice=&locale=zh_cn"
    headers = generate_random_headers()

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # print("Response JSON:", response.json())
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}, Response: {response.text}")


class Location:
    def __int__(self):
        self.ip = ''
        self.latitude = ''
        self.longitude = ''


if __name__ == "__main__":
    location_json = fetch_location_info()

    location = Location()
    location.ip = location_json['result']['ip']
    location.latitude = location_json['result']['location']['lat']
    location.longitude = location_json['result']['location']['lng']
    print(f'ip: {location.ip}')
    print(f'lat: {location.latitude}')
    print(f'lng: {location.longitude}')
    print('\t')

    weather_json = fetch_weather_info(location.latitude, location.longitude)
    print(weather_json)

    # 示例 JSON 文件路径
    json_file_path = './weather.json'
    # 将 Python 对象写入 JSON 文件
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(weather_json, file, indent=4, ensure_ascii=False)
