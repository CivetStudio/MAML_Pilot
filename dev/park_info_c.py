import time

import requests


headers = {
    "Host": "platform.52mengdong.com",
    "apptype": "applet-qq",
    "Accept": "*/*",
    "appname": "almanac",
    "timestamp": str(time.time()),
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "token": "",
    "Content-Type": "application/json",
    "versioncode": "28",
    "Referer": "https://appservice.qq.com/1110695537/0.2.8/page-frame.html",
    "User-Agent": "QQ/9.0.21.631 CFNetwork/1492.0.1 Darwin/23.3.0",
    "Connection": "keep-alive",
    "sign": "a904908a1eefecfd58779eaa6e720691"
}
url = "https://platform.52mengdong.com/platform/sign/zodiac/detail/1"
response = requests.get(url, headers=headers)

print(response.text)
print(response)