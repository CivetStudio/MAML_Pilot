import time
import os
from ninepatch import Ninepatch
import dev.Ninepatch.border


# 获取黑边数据
def get_chunk_info(ninepatch):
    t0 = ninepatch.marks['scale']['x'][0][0]
    t1 = ninepatch.marks['scale']['x'][0][1]
    t2 = t1 - t0
    # print(f'Top: （{t0}, {t1})')
    l0 = ninepatch.marks['scale']['y'][0][0]
    l1 = ninepatch.marks['scale']['y'][0][1]
    l2 = l1 - l0
    # print(f'Left: ({l0}, {l1})')
    b0 = ninepatch.marks['fill']['x'][0]
    b1 = ninepatch.marks['fill']['x'][1]
    b2 = b1 - b0
    # print(f'Bottom: ({b0}, {b1})')
    r0 = ninepatch.marks['fill']['y'][0]
    r1 = ninepatch.marks['fill']['y'][1]
    r2 = r1 - r0
    # print(f'Right: ({r0}, {r1})')

    chunk_info = {
        "Bottom": (b0, b1, b2),
        "Right": (r0, r1, r2),
        "Top": (t0, t1, t2),
        "Left": (l0, l1, l2)
    }

    return chunk_info


image_path = './test/myninepatch3.9.png'
ninepatch = Ninepatch(image_path)
output_temp_path = ''
chunk_info = {}

if ninepatch.content_area:
    # 通过检测拉伸区域，有黑边时自动渲染
    print(ninepatch.content_area)  # content_area(left=23, top=20, right=27, bottom=59)
    chunk_info = get_chunk_info(ninepatch)
else:
    # 无黑边时自动加入黑边
    # 获取文件名和扩展名
    filename, extension = os.path.splitext(image_path)
    # 创建临时文件名
    output_temp_path = filename.replace('.9', '') + '_temp.9' + extension
    print(output_temp_path)  # 输出 ./test/myninepatch2_temp.9.png
    dev.Ninepatch.border.main(image_path, output_temp_path)
    ninepatch = Ninepatch(output_temp_path)
    chunk_info = get_chunk_info(ninepatch)

print(chunk_info)
if chunk_info:
    # 渲染图片至特定尺寸
    scaled_image = ninepatch.render(512, 512)  # creates a new PIL image
    # 释放临时图片
    if os.path.exists(output_temp_path):
        os.remove(output_temp_path)
    # 显示渲染后的图像
    scaled_image.show()
