import warnings

# 忽略特定类型的警告
warnings.filterwarnings("ignore")

import json
from io import BytesIO
import requests
from PIL import Image

url = 'https://qsparking.com/vel/park/temp_pre_order'
url_car = 'https://qsparking.com/vel/user/cars'
authorization = 'hd c4e63d1298a7cff180e86eda7f9e3700'
headers = {
    # "Host": "qsparking.com",
    # "Accept": "*/*",
    "Authorization": f"{authorization}",
    # "Sec-Fetch-Site": "same-site",
    # "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    # "Accept-Encoding": "gzip, deflate, br",
    "Platform": "mobile",
    # "Sec-Fetch-Mode": "cors",
    # "Origin": "https://www.qsparking.com",
    # "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.47(0x18002f2c) NetType/WIFI Language/zh_CN",
    # "Referer": "https://www.qsparking.com/",
    # "Connection": "keep-alive",
    # "Content-Type": "application/json",
    # "Sec-Fetch-Dest": "empty",
    "Platform-type": "wx"
}

# data = {
#     'code': '',
#     'car_number': '闽AC3M02',
#     # 'car_number': '闽A8S40H'
# }
data = {}

response = requests.get(url_car, headers=headers)
decoded_response = response.text.encode('utf-8').decode('unicode-escape')
print('车牌列表:', decoded_response, '\n')
parsed_response = json.loads(response.text)
car_number = parsed_response['data']
for _car_ in car_number:
    data['car_number'] = _car_['car_number']
    response = requests.get(url, headers=headers, params=data)
    decoded_response = response.text.encode('utf-8').decode('unicode-escape')
    parsed_response = json.loads(response.text)
    # print(decoded_response)
    print(f"查询车牌：{data['car_number']}")
    print(parsed_response)

    # 检查是否存在 'data' 字段
    if 'data' in parsed_response:
        data_field = parsed_response['data']
        print(f"进场时间：{parsed_response['data']['ent_time']}")
        print(f"停车场名称：{parsed_response['data']['park_name']}")

        # 检查是否存在 'ent_pic' 字段
        if 'ent_pic' in data_field:
            # 获取图片 URL
            image_url = data_field['ent_pic']
            # 发送请求获取图片内容
            image_response = requests.get(image_url)
            # 将图片内容转换为 PIL Image 对象
            image = Image.open(BytesIO(image_response.content))
            # 弹出图片窗口显示
            # image.show()
        else:
            print("ent_pic parameter not found in the 'data' field.")
    else:
        print(f"{parsed_response['msg']}")
    print('\t')

# 恢复警告设置
# warnings.resetwarnings()
