import requests

# 定义要发送的文本数据
encoding = 'utf-8'
text_data = """<?xml version="1.0" encoding="utf-8"?>
<ROOT>
    <!-- 测试代码 -->
    <Image _psd="图片" x="0" y="0" src="assets/apng.png" />
    <FunCom target="Demo" params="{'a': '0', 'b': '1'}" />
</ROOT>
"""
encoded_data = text_data.encode(encoding)
# 发送 POST 请求给服务器
host = '192.168.0.19'
port = '9975'
host_name = '31ds6tk49329.vicp.fun'
# response = requests.post(f'http://{host}:{port}/api/send_text_data', data=encoded_data)
file_name = 'maml.xml'
with open(file_name, 'rb') as f:
    files = [('file', (file_name, f, 'application/xml'))]
    # response = requests.post(f'http://{host}:{port}/api/send_text_data', files=files)
    response = requests.post(f'http://{host_name}/api/send_text_data', files=files)

# 检查响应状态码是否为 200
if response.status_code == 200:
    # 将服务器返回的文本文件保存到本地
    with open('manifest.xml', 'wb') as f:
        response_content = response.content
        f.write(response_content)
    print('文本文件已保存为 manifest.xml')
else:
    print('服务器返回错误:', response.status_code)

 # curl -X POST -F "file=@maml.xmlƒ" http://192.168.0.19:9975/api/send_text_data > manifest.xml