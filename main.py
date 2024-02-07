#
#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |# '.
#                 / \\|||  :  |||# \
#                / _||||| -:- |||||- \
#               |   | \\\  -  #/ |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#               佛祖保佑         永无BUG
#
#
#

"""
03.30 需要修复使用 Slot 时，只能获取一行代码（目前的解决方案是用 <PlaceHolder name="Slot" /> 解决）
03.30 加入【TextSize】特殊用法
05.08 转移到 Mac 本地，去除【source.xml】及【maml.xml】，直接从剪贴板读取maml.xml，并将文件生成其对应目录下；修改 dll 为本地路径
      由于 Mac 没有 Temp文件夹

— — — — 待同步至 Windows — — — —

05.11 新增【WidgetSu】小部件代码模版
05.11 issue: PlaceHolder 多行传值 / Slot 传单值 PlaceHolder在每个lib只能有一个
05.15 issue important: .replace('#' + str(var_from_target[i]) + ', ' 逗号前去除空格 + '@'
05.16 修改 intent 库：浏览器, 计算器, 日历, 时钟
05.17 新增【var_from_target】数组: 收录 countName
05.19 新增全局变量【night_mode】（未同步至CivetCode）
06.16 修改WeekCalendar库：新增系统字体写法（旧版本可能导致报错）
06.17 新增【maml.xml】根标签【_splitExt="0"】【_splitGroup="0"】属性，当为 "0" 或 "false" 时不进行对应操作
        若不存在属性则默认开启（针对小米主题Rocks）
06.19 新增移除所有 alias 属性（PSD切图时产生的文件注释）
06.25 issue important：解决【Calendar】标签为【card="Almanac"】时，取消模块替换
06.27 issue important：在编写带有【market】属性的Intent时，需注意Props属性读取先后顺序（如美团、饿了么）
07.08 新增标签顺序整理 (preLoadVar, preLoadExt)：Lockscreen > ExternalCommands > VariableBinders > VariableAnimation >
        Var.threshold > Var > Weather > Calendar > Healthy > VarArray > CountDownTime > ... > Group.Button
        08.30 新增 CountDownTime 排序
07.14 新增模块属性【disabled】，该属性存在时，对应模块不进行编译
      优化数据库结构，清空使用次数及logging文件，已存放于su文件夹（2900 count）
07.14 打包为 Windows 与 macOS 客户端，版本更新至 V1.1
07.15 V1.2（发布）：加入【IntentMarket】函数，判断是否存在消息通知源处理 IntentCommand 跳转至小米应用商店
07.16 V1.3（发布）：新增【maml.xml】根标签【_preload="0"】属性，当为 "0" 或 "false" 时不进行对应操作

07.17 新增本地函数【calculateMemory】，预估计算锁屏包内存
07.20 新增maml.xml根标签【_getSource="0"】属性，当为 "0" 或 "false" 时不进行对应操作
08.29 在【IntentMarket】函数中加入华为图片缩放特殊处理：【 <Image isBackground="false" scaleType="fill" /> 】
08.30 在【IntentMarket】函数中加入vivo【category】处理：【 category="android.intent.category.LAUNCHER" 】
      针对【AniFrame】中的【time】属性进行 abs(int(eval())) 操作，使【mResumeSpeed】适应传统动画，修复【ResumeAni】闪屏问题
      为带动画的【Image】标签加入【name】属性（适用于vivo）
      移除所有空标签（如拆分Button后的Group）
      优化运行时 Print 输出数据
      定义一个函数【convert_to_unicode】用于将中文和特殊字符转换为 Unicode 字符串（仅对【getAlias】有效）
      在【calculateMemory】函数中，加入：删除目录下所有以._开头的文件以及.DS_Store文件
09.16 Widget模式下，将未使用的Function去除，
        首先查询XML下所有FunctionCommand标签的name属性，将所有值提取到数组中，
        再查询所有Function标签，找到name属性，如果改值未在刚刚的数组中，则删除该Function标签
09.17 利用编译后的变量名称唯一性，去除废弃【VariableAnimation】变量 _soup_final
09.19 在小部件模式下，通过变量动画自动改变帧率控制器【FramerateController】，获取最大时间
09.21 将【Unicode】方法转移至【_soup_final】下，修复转义字符串失效问题
10.02 新增【src_exp_mode】:将代码里的 srcid 写法转为 srcExp 写法（适用于华为）
10.10 **新增【order_xml_mode】：将代码里的属性按照自定义排序（搜索 End ）

// 2024
01.05 删除无用【VarArray】标签
    VarArray: {@/#}{name}
01.08 自动修复不带【name】属性的【threshold】/【*Animation】标签
01.17 重新整理【splitGroup】函数下的属性eval问题（避免#mResumeAni_值被加入按钮）
    简化按钮内属性表达式 simplify_expression()
    // BUG：未考虑到min max函数包含在内的情况（/Users/wangshilong/Downloads/萌星球/蔡晶/五福临门/国内版/OPPO/lockscreen/advance/maml.xml）
    // 02.05 使用新的函数 evalNum()
01.25 新增 C_Array 数组标签处理（支持 Image / Text / Button，原理即将元素中的 {#countName} 循环替换为 {count} 所对应的数字，算法同小米）
01.27 修复 C_Array 数组标签处理（需在变量混淆之前处理）
01.29 稍微修复 lib 随机后缀算法（目前只能有两个 _port模式 或者 无_port模式）
01.29 新增 lib_dom_id, lib_dom_input 变量，支持在插件上加入 _id 属性，形成代码后缀（Exam_CountDays_{_id})
    // BUG：目前会导致SysTime失效
    // BUG: 02.05 将 SysTime 标签前置
    // Done: 02.06 将 threshold 中的 Var 标签删除
02.01 新增 C_Array 数组标签写法 <C_Array begin="0" end="1" indexName="_i" ></C_Array> 可与 count 属性交替使用
    修复 ExternalCommands 合并数组生成冗余引号问题 e_soup
02.02 新增 Image['act'] 写法：act="{_action_: up|double|click},{_action_tag_id_}"
    <_action_tag_id_><VariableCommand /></_action_tag_id_>
    该写法在混淆前解析（相当于在不破坏 maml.xml 的情况下改动）

    // ⚠️需要改进的点：
    1.当缺少 ['w', 'h'] 属性时，能否从文件路径中寻找对应值（考虑srcid, srcExp）
    2.Dev

02.02 新增 C_Array 数组标签写法: 支持单条的 VariableCommand 命令（不可与其他标签共用）
    <C_Array count="4" indexName="index">
        <VariableCommand name="test_#index" expression="#index" type="number" />
    </C_Array>
    16:18 已修复为自动识别代码

// 检测图片是否在代码内：
    1. "pic.png": search directly
    2. if "_" in "pic_0.png":
        prefix = split("_")[0] = "pic"
        and search "pic.png" or "pic_" in code
// 检测 IntentCommand 中 package 与 class 是否都存在
    （VIEW除外）
// 需求：【Mask / Paint】从Group中提取
// 图片减半、重命名功能

⚠️历史遗留问题:
      1 四个空格转为/t
      2 &lt; &gt; 应该为&amp;lt &amp;gt
      3 lib文件夹下模块内变量名称混淆
"""


import logging
import os
import random
import re
import sys
import shutil
import sqlite3
import time
import xml.dom.minidom
import zlib
import pyperclip
import subprocess
from bs4 import BeautifulSoup, Comment
from lxml import etree as lxml
# import wx
# import requests

from splitTools import splitVar, splitExt, splitBinders, splitGroup, preLoadVar, preLoadExt, intentMarket

maml_main_xml = ''
win_local = 1
mac_local = 0
if 'PYCHARM_HOSTED' in os.environ and sys.platform.startswith('darwin') or win_local:
    # print("macOS or PyCharm")
    sys_version = 0
    current_dir = ''
    maml_main_xml = pyperclip.paste().replace('\\', '/').replace('"', '')
# if mac_local == 1:
#     # print("Windows or macOS")
#     sys_version = 1
#     current_dir = os.path.abspath(sys.argv[0]).replace('\\', '/') \
#         .replace('"', '').replace('main.exe', '').replace('main.py', '') \
#         .replace('MacOS/MamlPilot', 'MacOS')
#     # print(f'sys.argv: {sys.argv}')
#     if len(sys.argv) == 1:
#
#         sys_text = """MAML Pilot——全平台代码加密工具_20240206
# Designed by 灵貓 / Civet
#
# 请将XML文件名称改为【maml.xml】并拖入程序中
# 程序文件名请勿修改，修改后无法打开！反馈问题请联系QQ：1876461209
#
# 功能说明：
# 1.支持代码变量混淆，从Group组中拆分Var变量、Button按钮
# 2.代码标签自动排序：Lockscreen > ExternalCommands > VariableBinders > VariableAnimation > Var.threshold > Var > Weather > Calendar > Healthy > VarArray > ... > Group.Button
# 3.支持MIUI平台的config.xml及var_config.xml中的对应变量转译，只需将文件放于【maml.xml】的同一目录下即可
# 4.已涵盖全平台中的所有全局变量，不会导致锁屏功能失效问题（已试验10000+次）
# 5.后续将支持代码插件化功能，类似MIUI主题编辑器中的插件模块
# """
#
#         if sys.platform.startswith('darwin') and mac_local == 0:
#             # noinspection PyUnusedLocal
#             class MyFrame(wx.Frame):
#                 def __init__(self, parent, title):
#                     super().__init__(parent, title=title, size=(800, 500))
#                     panel = wx.Panel(self)
#
#                     text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
#                     text_ctrl.SetValue(sys_text)
#
#                     font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
#                     text_ctrl.SetFont(font)
#
#                     text_ctrl.SetForegroundColour(wx.WHITE)
#                     text_ctrl.SetBackgroundColour('#2b2b2c')
#
#                     sizer = wx.BoxSizer(wx.VERTICAL)
#                     sizer.Add(text_ctrl, proportion=1, flag=wx.EXPAND)
#                     panel.SetSizer(sizer)
#
#                     self.CenterOnScreen()
#                     self.Show()
#                     self.Bind(wx.EVT_CLOSE, self.on_close)  # 绑定 EVT_CLOSE 事件
#
#                 def on_close(self, event):  # 修正 on_close 方法的参数
#                     self.Destroy()
#
#
#             app = wx.App()
#             frame = MyFrame(None, "MAML Pilot 使用说明")
#             app.MainLoop()
#
#         else:
#             print(sys_text)
#             # print('\t')
#             # print('MAML Pilot——全平台代码加密工具_20230716_V1.3')
#             # print('Designed by 灵貓 / Civet')
#             # print('\t')
#             # print('请将XML文件名称改为【maml.xml】并拖入程序中')
#             # print('程序文件名请勿修改，修改后无法打开！反馈问题请联系QQ：1876461209')
#             # print('\t')
#             # print('功能说明：')
#             # print('1.支持代码变量混淆，从Group组中拆分Var变量、Button按钮')
#             # print('2.代码标签自动排序：Lockscreen > ExternalCommands > VariableBinders > VariableAnimation > '
#             #       'Var.threshold > Var > Weather > Calendar > Healthy > VarArray > ... > Group.Button')
#             # print('3.支持MIUI平台的config.xml及var_config.xml中的对应变量转译，只需将文件放于【maml.xml】的同一目录下即可')
#             # print('4.已涵盖全平台中的所有全局变量，不会导致锁屏功能失效问题（已试验2900次）')
#             # print('5.后续将支持代码插件化功能，类似MIUI主题编辑器中的插件模块')
#             # print('（本窗口5秒后自动关闭）')
#
#         # time.sleep(5)
#         # sys.exit(1)
#     if len(sys.argv) > 1:
#         file_path = sys.argv[1]
#         maml_main_xml = file_path.replace('\\', '/').replace('"', '')

maml_rule_file = "maml.xml"
maml_file_name = os.path.basename(maml_main_xml)
maml_folder_name = os.path.dirname(maml_main_xml).split('/')[-1]

# 判断 maml_file_name 是否以 maml_rule_file 结尾
if maml_rule_file not in maml_file_name:
    print(f"Error: File must be '{maml_rule_file}'")
    sys.exit(1)

print('\t')
print(f'Source: {maml_main_xml}')
print(f'Folder: {maml_folder_name}')

logging_path = os.path.join(current_dir, 'logs')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=os.path.join(logging_path, 'main.log'))

start_time = time.time()  # 记录开始时间

orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=1):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


BeautifulSoup.prettify = prettify

line = ''
lib_folder_name = os.path.join(current_dir, 'lib')
assets_folder_name = os.path.join(current_dir, 'assets')

# 创建lib文件夹
if not os.path.exists(lib_folder_name):
    os.makedirs(lib_folder_name)

# 创建assets文件夹
if not os.path.exists(assets_folder_name):
    os.makedirs(assets_folder_name)

# 连接到数据库
database_path = os.path.join(logging_path, 'db')
conn = sqlite3.connect(os.path.join(database_path, "counter.db"))
# 创建表格（如果不存在）
conn.execute('''CREATE TABLE IF NOT EXISTS counter
             (id INTEGER PRIMARY KEY,
             count INTEGER,
             source TEXT,
             compress_rate TEXT,
             run_time TEXT,
             dev_time TEXT);''')
# 读取计数器的值
cursor = conn.cursor()
cursor.execute('SELECT id FROM counter ORDER BY id DESC LIMIT 1')
count = cursor.fetchone()
if count is None:
    count = 1
else:
    cursor.execute('SELECT count FROM counter ORDER BY count DESC LIMIT 1')
    count = cursor.fetchone()
    count = int(count[0]) + 1
# 关闭数据库连接
conn.close()

lib = []
lib_soup_attr = []
lib_soup_attr_def = []
lib_soup_str = []
lib_slots_num = {}
lib_valueholder = []
lib_nameholder = []
lib_placeholder = []
lib_placeholder_attr = []
lib_placeholder_str = []
lib_placeholder_str2 = []
lib_slots_list2 = []
tags_lib = []
tags_str = []
tags_attr = []
tags_slots = []

lib_slots = []
lib_slots_list = []

var_from_xml = []
var_forbid_name = ['Almanac', 'Almanac.baiji', 'Almanac.caishen', 'Almanac.chenA', 'Almanac.chenB', 'Almanac.chongsha',
                   'Almanac.chouA', 'Almanac.chouB', 'Almanac.fushen', 'Almanac.ganzhi', 'Almanac.haiA', 'Almanac.haiB',
                   'Almanac.ji', 'Almanac.jishen', 'Almanac.maoA', 'Almanac.maoB', 'Almanac.nongli', 'Almanac.riwuxing',
                   'Almanac.shen12', 'Almanac.shenA', 'Almanac.shenB', 'Almanac.shengxiao', 'Almanac.siA',
                   'Almanac.siB', 'Almanac.taishen', 'Almanac.weiA', 'Almanac.weiB', 'Almanac.wuA', 'Almanac.wuB',
                   'Almanac.xingxiu28', 'Almanac.xiongshen', 'Almanac.xishen', 'Almanac.xuA', 'Almanac.xuB',
                   'Almanac.yangli', 'Almanac.yi', 'Almanac.yinA', 'Almanac.yinB', 'Almanac.yingui', 'Almanac.youA',
                   'Almanac.youB', 'Almanac.zhishen', 'Almanac.ziA', 'Almanac.ziB', 'BigEvent_0', 'BigEvent_0.event',
                   'BigEvent_0.year', 'BigEvent_1', 'BigEvent_1.event', 'BigEvent_1.year', 'BigEvent_2',
                   'BigEvent_2.event', 'BigEvent_2.year', 'BigEvent_3', 'BigEvent_3.event', 'BigEvent_3.year',
                   'BigEvent_4', 'BigEvent_4.event', 'BigEvent_4.year', 'ChargeSpeed', 'ChargeWireState',
                   'Constellations', 'Constellations.signName', 'Constellations.today.datetime',
                   'Constellations.today.healthStar', 'Constellations.today.loveDes', 'Constellations.today.loveStar',
                   'Constellations.today.luckyColor', 'Constellations.today.luckyNumber',
                   'Constellations.today.matchSign', 'Constellations.today.moneyDes', 'Constellations.today.moneyStar',
                   'Constellations.today.summaryDes', 'Constellations.today.summaryStar',
                   'Constellations.today.workDes', 'Constellations.today.workStar', 'MiStep', 'MiSteps',
                   'MiSteps_distance', 'MiSteps_energy', 'MiSteps_goal', 'MiSteps_steps', 'MiSteps_strength_duration',
                   'MiSteps_summary', 'Mi_begin_time', 'Mi_end_time', 'Mi_step', 'Progress', 'SetLanguage', 'Weather',
                   'Weather.today.aqivalue', 'Weather.today.aqivaluetext', 'Weather.today.carWashLevel',
                   'Weather.today.cnweatherDes', 'Weather.today.cnweatherid', 'Weather.today.coldLevel',
                   'Weather.today.currentTem', 'Weather.today.dressingLevel', 'Weather.today.humidity',
                   'Weather.today.maxtemp', 'Weather.today.mintemp', 'Weather.today.moonRise', 'Weather.today.moonSet',
                   'Weather.today.sportsLevel', 'Weather.today.sunRise', 'Weather.today.sunSet',
                   'Weather.today.weatherDes', 'Weather.today.weatherIcon', 'Weather.today.weatherIconDes',
                   'Weather.today.weatherid', 'Weather.today.winddir', 'Weather.today.winddirDes',
                   'Weather.tomorrow.aqivalue', 'Weather.tomorrow.aqivaluetext', 'Weather.tomorrow.carWashLevel',
                   'Weather.tomorrow.cnweatherDes', 'Weather.tomorrow.cnweatherid', 'Weather.tomorrow.coldLevel',
                   'Weather.tomorrow.currentTem', 'Weather.tomorrow.dressingLevel', 'Weather.tomorrow.humidity',
                   'Weather.tomorrow.maxtemp', 'Weather.tomorrow.mintemp', 'Weather.tomorrow.moonRise',
                   'Weather.tomorrow.moonSet', 'Weather.tomorrow.sportsLevel', 'Weather.tomorrow.sunRise',
                   'Weather.tomorrow.sunSet', 'Weather.tomorrow.weatherDes', 'Weather.tomorrow.weatherIcon',
                   'Weather.tomorrow.weatherIconDes', 'Weather.tomorrow.weatherid', 'Weather.tomorrow.winddir',
                   'Weather.tomorrow.winddirDes', 'Weather.yesterday.aqivalue', 'Weather.yesterday.aqivaluetext',
                   'Weather.yesterday.carWashLevel', 'Weather.yesterday.cnweatherDes', 'Weather.yesterday.cnweatherid',
                   'Weather.yesterday.coldLevel', 'Weather.yesterday.currentTem', 'Weather.yesterday.dressingLevel',
                   'Weather.yesterday.humidity', 'Weather.yesterday.maxtemp', 'Weather.yesterday.mintemp',
                   'Weather.yesterday.moonRise', 'Weather.yesterday.moonSet', 'Weather.yesterday.sportsLevel',
                   'Weather.yesterday.sunRise', 'Weather.yesterday.sunSet', 'Weather.yesterday.weatherDes',
                   'Weather.yesterday.weatherIcon', 'Weather.yesterday.weatherIconDes', 'Weather.yesterday.weatherid',
                   'Weather.yesterday.winddir', 'Weather.yesterday.winddirDes', '__android_version', 'night_mode',
                   'darkMode', '__darkmode', '__darkmode_wallpaper', '__maml_version', '__miui_version_code',
                   '__miui_version_name', '__thememanager_version', 'almanacRespCode', 'ampm',
                   'applied_light_wallpaper', 'aqi_level', 'automaticRotary', 'automaticRotaryValue', 'battery_level',
                   'battery_state', 'bigEventRespCode', 'call_missed_count', 'calories_value', 'cityid', 'cityname',
                   'cityname_en', 'cityname_tw', 'clock_button', 'constellationRespCode', 'constellationsId',
                   'cur_aqi_co', 'cur_aqi_level', 'cur_aqi_no', 'cur_aqi_no2', 'cur_aqi_o3', 'cur_aqi_so',
                   'cur_avg_aqi', 'cur_avg_pm25', 'cur_pm10', 'cur_pressure', 'cur_uv_desc', 'cur_uv_index',
                   'cur_visibility', 'cur_weather', 'cur_weather_direct', 'cur_weather_humidity', 'cur_weather_power',
                   'cur_weather_temp', 'cur_weather_type', 'date', 'date_lunar', 'day_temp', 'day_weather_type',
                   'defaultScreen_x', 'defaultScreen_y', 'deviceTime', 'distance_value', 'feast', 'festival',
                   'flashlight', 'flashlightValue', 'face_enable', 'face_detect_state_msg', 'face_detect_help_msg',
                   'fod_enable', 'fod_height', 'fod_state_msg', 'fod_width', 'fod_x', 'fod_y', 'frame_rate',
                   'hasSteps', 'hasWeather', 'hassteps', 'health1', 'heart_rate_value', 'hour', 'hour12', 'hour24',
                   'isPreviewMode', 'isMatePad_H_2560', 'isMatePad_V_1600', 'isSupportMicro',
                   'is_music_playing', 'is_work_day', 'ishour12', 'lunarDay', 'lunarMonth', 'lunarYear',
                   'lunar_solar_term', 'mCivetCode_000', 'mCivetCode_001', 'mCivetCode_002',
                   'mCivetCode_003', 'mCivetCode_004', 'mCivetCode_005', 'mCivetCode_006', 'mCivetCode_007',
                   'mCivetCode_008', 'mCivetCode_009', 'mCivetCode_010', 'mGlobalVar', 'mGlobalVar_2H', 'media_genres',
                   'media_like_status', 'media_loading_status', 'media_mode_status', 'media_play_status',
                   'media_subtitle', 'media_title', 'microPhone_state', 'microPhone_volume', 'microphone_state',
                   'minute', 'month', 'month_lunar', 'month_lunar_leap', 'musicPlayDuration', 'musicPlaySecond',
                   'musicTotalDuration', 'musicTotalSecond', 'music_active', 'music_album_cover', 'music_control',
                   'music_display', 'music_next', 'music_pause', 'music_play', 'music_prev', 'next_alarm_time',
                   'night_temp', 'night_weather_type', 'noticeDown', 'notification', 'ownerinfo', 'point_count',
                   'pollingTime', 'processCpuFree', 'processCpuRate', 'rain_probability', 'raw_screen_height',
                   'raw_screen_width', 'real_feel_temp', 'repeat_mode', 'resting_heart_rate_value', 'screen_density',
                   'second', 'shake', 'shake_record', 'x_acc', 'y_acc', 'z_acc',
                   'sms_unread_count', 'sport_value', 'step', 'step_today', 'steps_value',
                   'storageFree', 'storageFreeNum', 'storageTotal', 'storageTotalNum', 'sunrise_time', 'sunset_time',
                   'system.date', 'system.time.ampm', 'system.time.hour1', 'system.time.hour2', 'system.time.min1',
                   'system.time.min2', 'systemVersion', 'time', 'timeZone', 'time_format', 'time_sys',
                   'touch_begin_time', 'touch_begin_x', 'touch_begin_y', 'touch_pressure', 'touch_x', 'touch_y',
                   'vibration', 'view_height', 'view_width', 'volume_level', 'volume_level_old', 'volume_type',
                   'weather', 'weather1', 'weather2', 'weather3', 'weatherRespCode', 'weather_', 'weather_city',
                   'weather_condition', 'weather_cur_temp', 'weather_description', 'weather_high_temp', 'weather_id',
                   'weather_location', 'weather_low_temp', 'weather_publish_time', 'weather_sunrise', 'weather_sunset',
                   'weather_temperature', 'weather_tmphighs', 'weather_tmplows', 'weather_wind_dir', 'weather_wind_pow',
                   'year_lunar', 'year_lunar1864', 'year_lunar_leap', 'lunar_calendar_enable', 'battery_enable',
                   'notification_enable', 'preview_mode', 'connectedStatus', 'headsetName', 'headsetBatteryLevel']

var_alias_all = 1
var_alias = 0
var_alias_list = 1
var_alias_anti = 1

lib_slot_xml = "$.dll"
process_xml = "$0.dll"
parse_xml = "$1.dll"
success_xml = maml_main_xml.replace(maml_file_name, 'manifest.xml')
anti_xml = "antiAliasing.xml"
config_xml = maml_main_xml.replace(maml_file_name, 'config.xml')
var_config_xml = maml_main_xml.replace(maml_file_name, 'var_config.xml')
# var_config_xml = "var_config.xml"

# langs_id = 0
langs_id = 4 if os.path.exists(config_xml) or os.path.exists(var_config_xml) else 2
var_persist_attr = "const" if langs_id == 0 or langs_id == 4 else "persist"

# maml.xml > main.xml
# if os.path.exists('maml.xml'):
# 	maml_main_xml = 'maml.xml'
# elif os.path.exists('main.xml'):
# 	maml_main_xml = 'main.xml'
# else:
# 	maml_main_xml = 'maml.xml'
# 	maml_def_xml = '<?xml version="1.0" encoding="utf-8"?>\n<Lockscreen frameRate="240" screenWidth="1080" version="1" \
# 	 vibrate="false" _dev="civet" _devTime="$_devTime">\n\t<!-- 欢迎定制锁屏：灵貓 QQ 1876461209 -->\n\t<Su/>\n</Lockscreen>'
# 	with open(maml_main_xml, 'w', encoding='utf-8') as f0:
# 		f0.write(str(maml_def_xml))


# 获取网络时间戳
def getTimeSys():

    def get_wifi_ssid():
        try:
            # 使用 networksetup 命令来获取当前 Wi-Fi SSID
            wifi_result = subprocess.run(["/usr/sbin/networksetup", "-getairportnetwork", "en0"], capture_output=True, text=True)
            output = wifi_result.stdout.strip()
            ssid_name = output.split(":")[1].strip()
            return ssid_name
            # print(f"Wi-Fi SSID: {ssid_name}")
        except Exception as wifi_e:
            print(f"Wi-Fi Error: {wifi_e}")

    global wifi_state
    global wifi_in_vgoing

    wifi_state = bool(get_wifi_ssid() == "Redmi_71E5"
                      or get_wifi_ssid() == "Civet's iPhone"
                      or get_wifi_ssid() == "Xiaomi_4A3E"
                      or get_wifi_ssid() == "vgoing")

    wifi_in_vgoing = bool(get_wifi_ssid() == "vgoing")
    # print(wifi_state)

    timestamp_ms = int(time.time() * 1000)
    return timestamp_ms


# 生成随机16进制数字(length:[0,16])
def randomHex(length):
    random_result = '0x' + hex(random.randint(0, 16 ** length)).replace('0x', '').upper()
    if len(random_result) < length:
        random_result = '0' * (length - len(random_result)) + random_result
    return random_result


# 清理缓存文件
def cleanCacheBefore():
    if os.path.exists(anti_xml):
        os.remove(anti_xml)
    # if os.path.exists(success_xml):
    # 	os.remove(success_xml)
    if os.path.exists('manifest-src.xml'):
        os.remove('manifest-src.xml')


# 清理缓存文件
def cleanCache():
    if os.path.exists(lib_slot_xml):
        os.remove(lib_slot_xml)
    if os.path.exists(process_xml):
        os.remove(process_xml)
    if os.path.exists(parse_xml):
        os.remove(parse_xml)


cleanCacheBefore()
if not os.path.exists(success_xml):
    shutil.copy(maml_main_xml, success_xml)


# 获取所有库资源文件夹名称
def dirLib(is_lib_folder):
    for file in os.listdir(is_lib_folder):
        lib_dir = os.path.join(is_lib_folder, file)
        if os.path.isdir(lib_dir):
            lib.append(file.replace(is_lib_folder, ''))


# 获取库文件Attributes以及相应默认值
def getLib(lib_file):
    global lib_valueholder_num
    global lib_props_num
    global lib_slots_list2
    lib_valueholder_num = 0
    lib_props_num = 0

    if os.path.exists('' + lib_folder_name + '/' + lib_file + '/' + lib_file + '.xml'):
        lib_file_name = lib_file + '.xml'
    else:
        lib_file_name = 'manifest.xml'
    lib_soup = BeautifulSoup(open('' + lib_folder_name + '/' + lib_file + '/' + lib_file_name, encoding="utf-8"),
                             features="lxml-xml")

    if lib_soup.Props is not None:
        lib_valueholder_num = 0
        lib_props_num += 1
        for lib_tag in lib_soup.find_all(re.compile("item")):
            if lib_tag.parent.name == "Props":
                if lib_tag.get('name') is not None:
                    lib_soup_attr.append(lib_tag.get('name'))
                    lib_soup_attr_def.append(lib_tag.get('default'))
    elif lib_soup.ValueHolder is not None and lib_props_num == 0:
        lib_valueholder_num = 1
        for lib_tag in lib_soup.find_all('ValueHolder'):
            lib_valueholder.append(lib_tag)
            lib_soup_attr.append(lib_tag.get('name'))
            lib_soup_attr_def.append('')
        # if lib_tag.get('type') == 'string':
        # 	var_alias_all = 0
        # else:
        # 	var_alias_all = 1
        for lib_tag in lib_soup.find_all('NameHolder'):
            lib_nameholder.append(lib_tag.get('name'))

    # print('Current lib_valueholder_num: ', lib_valueholder_num, lib_file)

    if lib_soup.PlaceHolder is not None:
        for lib_tag in lib_soup.find_all('PlaceHolder'):
            lib_placeholder.append(lib_tag)
            lib_placeholder_attr.append(lib_tag.get('name'))
        # print('lib_placeholder: ', lib_placeholder, '\n')
        # print('lib_placeholder_attr: ', lib_placeholder_attr, '\n')

    if lib_soup.Slots is not None:
        for lib_slot in lib_soup.find_all('Slots'):
            lib_slot['id'] = randomHex(8)
            lib_slots_list.append(str(lib_slot.get('slotName')))
            lib_slots_list2 = list(set(lib_slots_list))
        # print(lib_slots_list2)
        lib_slots_num[lib_file] = len(lib_slots_list2)
        if len(lib_slots_list):
            lib_slots_list.clear()
        if len(lib_slots_list2):
            lib_slots_list2.clear()
    else:
        lib_slots_num[lib_file] = 0
    return


# 获取库文件主内容并替换Attributes
def getLibContent(lib_file_main, soup_dom_id=0, soup_dom_input=None):
    tags_lib.reverse()
    tags_str.reverse()
    tags_attr.reverse()
    lib_soup_attr.reverse()
    lib_soup_attr_def.reverse()

    if os.path.exists('' + lib_folder_name + '/' + lib_file_main + '/' + lib_file_main + '.xml'):
        lib_file_name = lib_file_main + '.xml'
    else:
        lib_file_name = 'manifest.xml'
    lib_soup = BeautifulSoup(open('' + lib_folder_name + '/' + lib_file_main + '/' + lib_file_name, encoding="utf-8"),
                             features="lxml-xml")

    for lib_slot in lib_soup.find_all('Slots'):
        lib_slot['id'] = randomHex(8)
        lib_slots.append(str(lib_slot))
    # for lib_slot in lib_soup.find_all('PlaceHolder'):
    # 	if lib_slot['name'] == lib_placeholder:
    # 		lib_slot.parent.append(lib_placeholder_str)
    # 		lib_slot.decompose()
    with open(lib_slot_xml, 'w', encoding='utf-8') as _f0:
        if len(tags_slots):
            for _j in range(len(lib_slots)):
                if len(tags_slots) < len(lib_slots):
                    tags_slots.insert(len(tags_slots), "")
                lib_soup = str(lib_soup).replace(str(lib_slots[_j]), str(tags_slots[_j]))
        # if len(tags_slots) > len(lib_slots):
        # 	tags_slots_str = ''
        # 	for j in range(len(tags_slots)):
        # 		tags_slots_str = tags_slots_str + str(tags_slots[j])
        # 	lib_soup = str(lib_soup).replace(str(lib_slots[0]), tags_slots_str)
        else:
            for _j in range(len(lib_slots)):
                lib_soup = str(lib_soup).replace(str(lib_slots[_j]), '')
        if len(lib_placeholder_str2):
            for _k in range(len(lib_placeholder)):
                lib_soup = str(lib_soup).replace(str(lib_placeholder[_k]), str(lib_placeholder_str2[_k]))
            # <PlaceHolder name="ResumeAniCommand"/>
            # print(str(lib_placeholder[_k]))
        _f0.write(str(lib_soup))

    # print(lib_placeholder)
    # print(lib_placeholder_str2)

    if lib_valueholder_num == 0:
        lib_starts_with = '$'
    else:
        lib_starts_with = ''

    with open(lib_slot_xml, 'r', encoding='utf-8') as _f:
        with open(process_xml, 'w', encoding='utf-8') as _f2:
            for _line in _f:
                for _i in range(len(lib_soup_attr)):
                    if lib_valueholder_num == 0:
                        for _j in range(len(tags_attr)):
                            # 改动多次 慎重
                            if tags_attr[_j] is None or tags_attr[_i] is None:
                                _line = _line.replace(lib_starts_with + lib_soup_attr[_i], lib_soup_attr_def[_i])
                            else:
                                _line = _line.replace(lib_starts_with + lib_soup_attr[_i], str(tags_attr[_i]))
                    else:
                        # print(lib_soup_attr, tags_attr)
                        _line = _line.replace(lib_starts_with + lib_soup_attr[_i], tags_attr[_i])
                    # print(2)
                _f2.write(_line)
            # print(line)

    # 模块内变量名称混淆

    # # 筛选name及target，并添加后缀（6位随机数）

    _soup = BeautifulSoup(open(process_xml, encoding="utf-8"), features="lxml-xml")

    # 找出包含【name=""】
    for _tag in _soup.find_all(name=True):
        if _tag.get('name') is not None and _tag.get('name') != '' and _tag.name != "Extra" and not str(
                _tag.get('name')).startswith("$") and not str(_tag.get('name')).endswith("$"):
            if _tag.name == 'ValueHolder':
                # and 'Src' not in str(_tag.get('name'))
                if _tag.get('type') != 'string':
                    # 当 type 为 string 时，该属性不加入混淆
                    var_from_xml.append(_tag.get('name'))
            # elif tag.name == 'item' and eval(tag.get('default')):
            # 	var_from_xml.append(tag.get('name'))
            else:
                var_from_xml.append(_tag.get('name'))

    # 找出包含【dependency=""】
    for _tag in _soup.find_all(dependency=True):
        if _tag.get('dependency') is not None and _tag.get('dependency') != '' and _tag.name != "Extra" and not str(
                _tag.get('dependency')).startswith("$") and not str(_tag.get('dependency')).endswith("$"):
            var_from_xml.append(_tag.get('dependency'))

    # 找出包含【indexName=""】
    for _tag in _soup.find_all(indexName=True):
        if _tag.get('indexName') is not None and _tag.get('indexName') != '':
            var_from_xml.append(_tag.get('indexName'))

    # 找出包含【countName=""】
    for _tag in _soup.find_all(countName=True):
        if _tag.get('countName') is not None and _tag.get('countName') != '':
            var_from_xml.append(_tag.get('countName'))

    # 找出包含【target=""】
    for _tag in _soup.find_all(target=True):
        if _tag.get('target') is not None:
            for _i in range(len(var_from_xml)):
                target_save = str(_tag.get('target').replace('.visibility', '').replace('.animation', ''))
                if target_save != var_from_xml[_i] and len(target_save) >= 0:
                    var_from_xml.append(target_save)

    # soup_dom_str = str(soup.prettify(indent_width=1)).replace('    ', '\t')

    # 整理排序 + 去除系统变量
    var_from_target = list(set(var_from_xml).difference(set(var_forbid_name)))

    # 根据元素长度排序（从长到短）
    var_from_target.sort(key=lambda x: (len(x), x), reverse=True)

    # print('var_from_target: ', var_from_target, '\n')

    soup_dom_str = str(_soup.prettify(indent_width=1)).replace('    ', '\t')

    # 循环替换变量
    if var_alias_all == 1:

        # lib 随机后缀算法
        if var_alias != 1:
            if soup_dom_id:
                soup_dom_hex = soup_dom_input
            else:
                # soup_dom_hex = 'm' + hex(zlib.crc32(str(lib_file_name).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = randomHex(8).replace('0x', '').lower()
            # print(lib_file_name, soup_dom_hex)
        else:
            soup_dom_hex = ''
        # print(lib_file_name)

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace(' name="' + str(var_from_target[_i]) + '"',
                                                ' name="' + soup_dom_concat + soup_dom_hex + '"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace(' target="' + str(var_from_target[_i]) + '"',
                                                ' target="' + soup_dom_concat + soup_dom_hex + '"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace(' dependency="' + str(var_from_target[_i]) + '"',
                                                ' dependency="' + soup_dom_concat + soup_dom_hex + '"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace(' indexName="' + str(var_from_target[_i]) + '"',
                                                ' indexName="' + soup_dom_concat + soup_dom_hex + '"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace(' countName="' + str(var_from_target[_i]) + '"',
                                                ' countName="' + soup_dom_concat + soup_dom_hex + '"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace(' src="' + str(var_from_target[_i]) + '.artwork"',
                                                ' src="' + soup_dom_concat + soup_dom_hex + '.artwork"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace(' strPara="\'' + str(var_from_target[_i]) + '\'"',
                                                ' strPara="\'' + soup_dom_concat + soup_dom_hex + '\'"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '"',
                                                '#' + soup_dom_concat + soup_dom_hex + '"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '"',
                                                '@' + soup_dom_concat + soup_dom_hex + '"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + ')',
                                                '#' + soup_dom_concat + soup_dom_hex + ')')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '+',
                                                '#' + soup_dom_concat + soup_dom_hex + '+')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '-',
                                                '#' + soup_dom_concat + soup_dom_hex + '-')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '*',
                                                '#' + soup_dom_concat + soup_dom_hex + '*')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '/',
                                                '#' + soup_dom_concat + soup_dom_hex + '/')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '%',
                                                '#' + soup_dom_concat + soup_dom_hex + '%')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '=',
                                                '#' + soup_dom_concat + soup_dom_hex + '=')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '=',
                                                '@' + soup_dom_concat + soup_dom_hex + '=')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '}',
                                                '#' + soup_dom_concat + soup_dom_hex + '}')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '}',
                                                '@' + soup_dom_concat + soup_dom_hex + '}')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '{',
                                                '#' + soup_dom_concat + soup_dom_hex + '{')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '{',
                                                '@' + soup_dom_concat + soup_dom_hex + '{')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '!',
                                                '#' + soup_dom_concat + soup_dom_hex + '!')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '!',
                                                '@' + soup_dom_concat + soup_dom_hex + '!')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '[',
                                                '#' + soup_dom_concat + soup_dom_hex + '[')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '[',
                                                '@' + soup_dom_concat + soup_dom_hex + '[')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('[#' + str(var_from_target[_i]) + ']',
                                                '[#' + soup_dom_concat + soup_dom_hex + ']')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('[@' + str(var_from_target[_i]) + ']',
                                                '[@' + soup_dom_concat + soup_dom_hex + ']')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + ',',
                                                '#' + soup_dom_concat + soup_dom_hex + ',')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '.',
                                                '#' + soup_dom_concat + soup_dom_hex + '.')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + ' ',
                                                '#' + soup_dom_concat + soup_dom_hex + ' ')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + ')',
                                                '@' + soup_dom_concat + soup_dom_hex + ')')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '+',
                                                '@' + soup_dom_concat + soup_dom_hex + '+')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + ',',
                                                '@' + soup_dom_concat + soup_dom_hex + ',')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '.',
                                                '@' + soup_dom_concat + soup_dom_hex + '.')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + ' ',
                                                '@' + soup_dom_concat + soup_dom_hex + ' ')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('src="' + str(var_from_target[_i]) + '"',
                                                'src="' + soup_dom_concat + soup_dom_hex + '"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('"' + str(var_from_target[_i]) + '.animation',
                                                '"' + soup_dom_concat + soup_dom_hex + '.animation')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('"' + str(var_from_target[_i]) + '.visibility',
                                                '"' + soup_dom_concat + soup_dom_hex + '.visibility')

    # print('soup_dom_str: ', soup_dom_str, '\n')
    # 定义正则表达式，匹配形如【$*$】的全局变量
    soup_pattern = re.compile(r'\$(.*?)\$')
    soup_dom_str = re.sub(soup_pattern, r'\1', soup_dom_str)

    with open(process_xml, 'w', encoding='utf-8') as _f0:
        _f0.write(soup_dom_str)
    # print(soup_dom_str)

    # if var_alias_anti == 1:
    #
    #     var_from_target.sort(reverse=False)
    #     # print('var_from_target: ', var_from_target, '\n')
    #     alias_str = '<AntiAliasing version="1"></AntiAliasing>'
    #     _soup = BeautifulSoup(alias_str, features="lxml-xml")
    #     for alias in _soup.find_all('AntiAliasing'):
    #         for _j in range(len(var_from_target)):
    #             alias_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_j]).encode('UTF-8')))[2:].capitalize()
    #             alias_dom_hex = 'm' if len(alias_dom_concat) == 8 else ''
    #             alias_str_new = _soup.new_tag('Aliasing', initial=str(var_from_target[_j]), after=str(alias_dom_concat + alias_dom_hex))
    #             alias.append(alias_str_new)
    #
    #     with open(anti_xml, 'w', encoding='utf-8') as _f0:
    #         _f0.write(str(_soup.prettify(indent_width=1)).replace('    ', '\t'))
    #
    # else:
    #     if os.path.exists(anti_xml): os.remove(anti_xml)

    removeLibProps(process_xml, process_xml)
    return


# 移除库文件中的Props标签
def removeLibProps(lib_remove_in, lib_remove_out):
    tree = lxml.parse(lib_remove_in)
    _root = tree.getroot()
    if lib_props_num != 0:
        for Props in _root.findall("Props"):
            _root.remove(Props)
    elif lib_valueholder_num != 0:
        for ValueHolder in _root.findall("ValueHolder"):
            _root.remove(ValueHolder)
        for NameHolder in _root.findall("NameHolder"):
            _root.remove(NameHolder)
        for PlaceHolder in _root.findall("PlaceHolder"):
            _root.remove(PlaceHolder)
    tree = lxml.ElementTree(_root)
    tree.write(lib_remove_out, encoding="utf-8", xml_declaration=True)
    tree_str = lxml.tostring(_root, encoding='unicode').replace('<Template>', '').replace('</Template>', '').replace(
        '<ROOT>', '').replace('</ROOT>', '').replace('\n', '').replace('\t', '')
    # print(tree_str, lib_remove_in)
    lib_soup_str.append(tree_str)
    lib_soup_str.reverse()
    return


# 移除库文件中的Props标签
# def removeLibProps(lib_remove_in, lib_remove_out):
#     with open(lib_remove_in, 'r', encoding='utf-8') as file:
#         soup = BeautifulSoup(file, features='lxml-xml')
#
#     # root = soup.find('ROOT')  # 找到根元素
#     #
#     # props_tags = root.find_all('Props')
#     # for props in props_tags:
#     #     props.decompose()
#
#     props_tags = soup.find_all('Props')
#     valueholder_tags = soup.find_all('ValueHolder')
#     nameholder_tags = soup.find_all('NameHolder')
#     placeholder_tags = soup.find_all('PlaceHolder')
#
#     for tag in valueholder_tags + nameholder_tags + placeholder_tags:
#         tag.decompose()
#
#     with open(lib_remove_out, 'w', encoding='utf-8') as file:
#         file.write(str(soup))
#
#     tree_str = str(soup).replace('<Template>', '').replace('</Template>', '').replace('<ROOT>', '').\
#         replace('</ROOT>', '').replace('\n', '').replace('\t', '')
#     lib_soup_str.append(tree_str)
#     lib_soup_str.reverse()
#     return

# 解析XML文件，重新整理属性
def parseXML(parse_file_0, parse_file_1):
    _soup = BeautifulSoup(open(parse_file_0, encoding="utf-8"), features="lxml-xml")

    comments = _soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    _dev_time = getTimeSys()
    _soup_indent = str(_soup.prettify(indent_width=1)).replace('\n', '').replace('$_devTime', str(_dev_time))

    with open(parse_file_1, 'w', encoding='utf-8') as _f0:
        _f0.write(_soup_indent)
    return


# 保存XML文件，minidom格式化处理
def saveXML(save_file):
    global var_split_ext
    global var_split_group
    global var_alias

    # minidom格式化

    if line != '':
        _soup_indent = xml.dom.minidom.parseString(line)
        soup_dom_str = _soup_indent.toprettyxml()
    # print('soup_dom_str: ?', soup_dom_str)
    else:
        _soup_indent = BeautifulSoup(open(parse_xml, encoding="utf-8"), features="lxml-xml")
        # soup_dom_str = str(soup_indent).replace('&amp;', '&amp;amp;') 稳定，不敢动
        # soup_dom_str = str(soup_indent).replace('&gt;', '&amp;gt;') 稳定，不敢动
        soup_dom_str = str(_soup_indent).replace('&lt;', '&amp;lt;')
    # 	soup_dom_str = soup_dom_str.replace('\t \n', '\n').replace('\n\n\t', '\n\t')
    print('\t')
    print(f"LangsId: {langs_id}")
    print(f'Root: {manifest_root}')
    print(f'Width: {manifest_sw}')
    print(f'Height: {manifest_sh}')
    soup_dom_str = soup_dom_str.replace(manifest_root, 'Lockscreen')
    soup_dom_str = soup_dom_str.replace('persist_const', var_persist_attr)

    _soup = BeautifulSoup(soup_dom_str, features="lxml-xml")
    comments = _soup.find_all(string=lambda _text: isinstance(_text, Comment))

    # 去除注释
    for comment in comments:
        comment.extract()

    # 根据alias属性来判断是否混淆代码
    if _soup.Lockscreen.get('compiler') == 'false':
        var_alias = 0
    else:
        var_alias = 1

    global var_get_source

    var_split_ext = 1
    var_split_group = 1
    # var_preload = 1
    var_get_source = 0

    var_split_ext = 0 if str(_soup.Lockscreen.get('_splitExt')).upper() == "FALSE" or _soup.Lockscreen.get(
        '_splitExt') == "0" else 1
    print(f'Root[_splitExt]: {var_split_ext}')

    var_split_group = 0 if str(_soup.Lockscreen.get('_splitGroup')).upper() == "FALSE" or _soup.Lockscreen.get(
        '_splitGroup') == "0" else 1
    print(f'Root[_splitGroup]: {var_split_group}')

    var_preload = 0 if str(_soup.Lockscreen.get('_preload')).upper() == "FALSE" or _soup.Lockscreen.get(
        '_preload') == "0" else 1
    print(f'Root[_preload]: {var_preload}')

    var_get_source = 1 if str(_soup.Lockscreen.get('_getSource')).upper() == "TRUE" or _soup.Lockscreen.get(
        '_getSource') == "1" else 0
    print(f'Root[_getSource]: {var_get_source}')

    if _soup.Lockscreen.get('_splitExt') is not None:
        del _soup.Lockscreen['_splitExt']
    if _soup.Lockscreen.get('_splitGroup') is not None:
        del _soup.Lockscreen['_splitGroup']
    if _soup.Lockscreen.get('_preload') is not None:
        del _soup.Lockscreen['_preload']
    if _soup.Lockscreen.get('_getSource') is not None:
        del _soup.Lockscreen['_getSource']

    if manifest_root == 'Lockscreen' and langs_id != 4 or manifest_root == 'Widget':

        # TextSize处理
        # text_size = []
        for text in _soup.find_all('TextSize'):
            text_size = text.get('value', '100').split(', ')
            for _t in range(len(text_size)):
                text_size_var = _soup.new_tag('Var')
                text_size_var['name'] = str(text.get('_port', 'mTextSize_')) + str(text_size[_t])
                text_size_var['expression'] = f'int(sqrt({text_size[_t]})*#mTextSize_Var)'
                # text_size_var['type'] = 'number'
                print(f'TextSize: {text_size_var}')
                text.insert_before(text_size_var)
            text.decompose()

        # <TextSize alias="系统字体" _port="mTextSize_" value="100,90,80,70,60,50" />
        # <Var name="mTextSize_TextSizeVal_1" expression="int(sqrt(TextSizeVal_1)*#mTextSize_Var)" type="number" />

        # DateTime自动获取
        for date_time in _soup.find_all('DateTime'):
            date_time_size = str(date_time.get('size'))
            if str('"mTextSize_' + date_time_size + '"') not in str(_soup) and date_time_size.isnumeric():
                date_time_var = _soup.new_tag('Var')
                date_time_var['name'] = 'mTextSize_' + date_time_size
                date_time_var['expression'] = f'int(sqrt({date_time_size})*#mTextSize_Var)'
                print(f'DateTimeVar: {date_time_var}')
                _soup.Lockscreen.append(date_time_var)

        # Text自动获取
        for text_tag in _soup.find_all('Text'):
            text_tag_size = str(text_tag.get('size'))
            if str('"mTextSize_' + text_tag_size + '"') not in str(_soup) and text_tag_size.isnumeric():
                text_tag_var = _soup.new_tag('Var')
                text_tag_var['name'] = 'mTextSize_' + text_tag_size
                text_tag_var['expression'] = f'int(sqrt({text_tag_size})*#mTextSize_Var)'
                print(f'TextVar: {text_tag_var}')
                _soup.Lockscreen.append(text_tag_var)

        # C_Array 数组标签处理
        from tools.array import c_array
        for code in _soup.find_all('C_Array'):
            # print(code)
            c_array_r = c_array(str(code))
            # print(c_array_r)
            code.insert_after(c_array_r)
            code.extract()

        # 若 Image['rotation'] == '0' del Image['pivotX'], Image['pivotY'], Image['rotation'] // HONOR
        for image in _soup.find_all('Image'):
            image_w = image.get('w')
            image_h = image.get('h')
            image_px = image.get('pivotX')
            image_py = image.get('pivotY')
            image_r = image.get('rotation')
            if image_r == '0':
                del image['rotation']
                if image_px == f"{image_w}/2" and image_py == f"{image_h}/2":
                    del image['pivotX'], image['pivotY']
            if image.get('act'):
                _action = image.get('act')
                _action_ = str(_action.split(',')[0])
                _action_tag_id_ = str(_action.split(',')[1])
                # print(_action_, _action_tag_id_)

                for ac in _soup.find_all():
                    if ac.name == _action_tag_id_:
                        _action_condition = ac.get('condition')
                        # ac_contents = [str(item).replace('\n', '') for item in ac.contents]
                        ac_contents = [item for item in ac.contents if item != '\n']

                        _action_content = str(ac_contents).replace('[', '').replace(']', '')

                        # _action_content = str(ac).replace(f'<{_action_tag_id_}>', '').replace(f'</{_action_tag_id_}>', '')
                        # print(_action_content)
                        ac.extract()
                # _action_content = BeautifulSoup(_action_content, 'lxml-xml')

                # 创建 Button 标签
                _action_button = _soup.new_tag('Button')
                _action_triggers = _soup.new_tag('Triggers')
                _action_trigger = _soup.new_tag('Trigger')
                _action_trigger['action'] = _action_
                if _action_condition:
                    _action_trigger['condition'] = _action_condition
                _action_button.append(_action_triggers)
                _action_button.Triggers.append(_action_trigger)
                _action_button.Triggers.Trigger.append(_action_content)

                # 获取 Button 参数
                _action_button_x = image.get('x', '0')
                _action_button_y = image.get('y', '0')
                _action_button_w = image.get('w', '1')
                _action_button_h = image.get('h', '1')
                _action_button_align = image.get('align', 'left')
                _action_button_alignV = image.get('alignV', 'top')
                if _action_button_align == 'center':
                    _action_button_x = f"{_action_button_x}-int({_action_button_w}/2)"
                elif _action_button_align == 'right':
                    _action_button_x = f"{_action_button_x}-int({_action_button_w})"

                if _action_button_alignV == 'center':
                    _action_button_y = f"{_action_button_y}-int({_action_button_h}/2)"
                elif _action_button_alignV == 'bottom':
                    _action_button_y = f"{_action_button_y}-int({_action_button_h})"

                _action_button['x'] = _action_button_x
                _action_button['y'] = _action_button_y
                _action_button['w'] = _action_button_w
                _action_button['h'] = _action_button_h

                # print(_action_button)
                image.insert_after(_action_button)
                del image['act']

        print('\t')

    # Var.Trigger是否为空 --04.13 //内存可优化?:Test
    for var in _soup.find_all('Var'):
        if var.get('threshold') is not None:
            # if 'threshold' in str(var):
            var_contents = list(set(var.Trigger.contents))
            if var_contents == ['\n']:
                var.decompose()

    soup_dom_str = str(_soup.prettify(indent_width=1)).replace('    ', '\t') \
        # .replace(' _splitExt="0"', '').replace(' _splitGroup="0"', '').replace(' _preload="0"', '')

    with open(save_file, 'w', encoding='utf-8') as _f0:
        _f0.write(soup_dom_str)

    # 包含Var的Group数量(层级)
    # var_group = []
    # for group in soup.find_all('Group'):
    # 	var_group.append(group.find_all('Var'))
    # var_group_num = len(var_group)

    # 在Group里的Var数量
    var_str = []
    for var in _soup.find_all('Var'):
        if var.parent.name == 'Group':
            var_str.append(var)
    var_str_num = len(var_str)

    # ExternalCommands的数量
    # ext_com = soup.find_all('ExternalCommands')
    # ext_com_num = len(ext_com)

    # VariableBinders的数量
    var_binders = _soup.find_all('VariableBinders')
    var_binders_num = len(var_binders)

    if var_str_num > 0: splitVar(success_xml, success_xml)
    # if ext_com_num >= 1: splitExt(success_xml)
    if var_split_ext: splitExt(success_xml)
    if var_binders_num > 1: splitBinders(success_xml)
    if var_preload: preLoadVar(success_xml)
    if var_preload: preLoadExt(success_xml)
    if var_split_group: splitGroup(success_xml, manifest_root)
    intentMarket(success_xml)

    return


# 对指定目录进行递归遍历，判空删除
def removeEmpty(path):
    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        if os.path.isdir(folder_path):
            removeEmpty(folder_path)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)


# 加密XML文件
def getAlias():
    global config_soup_str, var_config_soup_str
    _var_from_xml = []

    _var_alias_all = 1
    # var_alias = 1
    _success_xml = maml_main_xml.replace(maml_file_name, 'manifest.xml')
    _origin_xml = "source.xml"
    _anti_xml = "anti.xml"
    _anti_list_xml = "disable.xml"
    _source_xml = maml_main_xml.replace(maml_file_name, _origin_xml)

    # shutil.copy2(_success_xml, _origin_xml)

    # # 筛选name及target，并添加后缀（6位随机数）

    _soup = BeautifulSoup(open(_success_xml, encoding="utf-8"), features="lxml-xml")
    for _root in _soup.find_all(True, limit=1):
        for _tag in _root.find_all(True, limit=1):
            comment = _soup.new_string(" 欢迎定制锁屏：灵貓 QQ 1876461209  /  Welcome to customize the lock screen: Civet QQ 1876461209 ", Comment)
            _tag.insert_before(comment)
            comment = _soup.new_string(
                " 违规抄袭将依据《中华人民共和国民法典》《中华人民共和国民法通则》《中华人民共和国著作权法》《计算机软件保护条例》《软件产品管理办法》《侵权责任法》《中华人民共和国知识产权法》追究法律责任  /  Illegal plagiarism will be investigated for legal liability in accordance with the Civil Code of the People's Republic of China. ",
                Comment)
            _tag.insert_before(comment)

    # print('Comment')

    # 找出包含【name=""】
    for _tag in _soup.find_all(name=True):
        if _tag.get('name') is not None and _tag.get('name') != '' and _tag.name != "Extra" and not str(
                _tag.get('name')).startswith("$") and not str(_tag.get('name')).endswith("$"):
            if _tag.name == 'ValueHolder':
                if _tag.get('type') != 'string':
                    _var_from_xml.append(_tag.get('name'))
            # elif tag.name == 'item' and eval(tag.get('default')):
            # 	var_from_xml.append(tag.get('name'))
            else:
                _var_from_xml.append(_tag.get('name'))

    # print('Name')

    # 找出包含【dependency=""】
    for _tag in _soup.find_all(dependency=True):
        if _tag.get('dependency') is not None and _tag.get('dependency') != '' and _tag.name != "Extra" and not str(
                _tag.get('dependency')).startswith("$") and not str(_tag.get('dependency')).endswith("$"):
            _var_from_xml.append(_tag.get('dependency'))

    # print('Dependency')

    # 找出包含【indexName=""】
    for _tag in _soup.find_all(indexName=True):
        if _tag.get('indexName') is not None and _tag.get('indexName') != '':
            _var_from_xml.append(_tag.get('indexName'))

    # print('indexName')

    # 找出包含【countName=""】
    for _tag in _soup.find_all(countName=True):
        if _tag.get('countName') is not None and _tag.get('countName') != '':
            _var_from_xml.append(_tag.get('countName'))

    # print('countName')

    # 找出包含【target=""】
    # for tag in soup.find_all(target=True):
    # 	if tag.get('target') is not None:
    # 		for i in range(len(var_from_xml)):
    # 			target_save = str(tag.get('target').replace('.visibility', '').replace('.animation', ''))
    # 			if target_save != var_from_xml[i] and len(target_save) >= 0:
    # 				var_from_xml.append(target_save)

    # print(var_from_xml)

    # soup_dom_str = str(soup.prettify(indent_width=1)).replace('    ', '\t')

    # 整理排序数组 + 去除系统变量
    var_from_target = list(set(_var_from_xml).difference(set(var_forbid_name)))

    # 根据元素长度排序（从长到短）
    var_from_target.sort(key=lambda x: (len(x), x), reverse=True)

    # print(var_from_target)

    soup_dom_str = str(_soup.prettify(indent_width=1)).replace('    ', '\t').replace('&amp;#', '&#')

    # 循环替换变量
    if _var_alias_all == 1:

        # 创建一个空字典并为每个数组的值分配默认值
        alias_dict = {}

        for var in var_from_target:
            alias_dom_concat = 'm' + hex(zlib.crc32(str(var).encode('UTF-8')))[2:].capitalize()
            alias_dom_hex = 'm' if len(alias_dom_concat) == 8 else ''
            alias_str_new = str(alias_dom_concat + alias_dom_hex)
            alias_dict[alias_str_new] = var

        if var_alias != 1:
            soup_dom_hex = randomHex(8).replace('0x', '').lower()
        else:
            soup_dom_hex = ''

        # 检测【config.xml】是否存在
        if os.path.exists(config_xml):
            if not os.path.exists(config_xml.replace('/config.xml', '/__config.xml')):
                shutil.copy2(config_xml, config_xml.replace('/config.xml', '/__config.xml'))

            # 重新解析XML
            config_soup = BeautifulSoup(open(config_xml, encoding="utf-8"), features="lxml-xml")
            config_soup_str = str(config_soup)

        # 检测【var_config.xml】是否存在
        if os.path.exists(var_config_xml):
            if not os.path.exists(var_config_xml.replace('/var_config.xml', '/__var_config.xml')):
                shutil.copy2(var_config_xml, var_config_xml.replace('/var_config.xml', '/__var_config.xml'))

            # 重新解析XML
            var_config_soup = BeautifulSoup(open(var_config_xml, encoding="utf-8"), features="lxml-xml")
            var_config_soup_str = str(var_config_soup)

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            # soup_dom_hex = hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
            soup_dom_str = soup_dom_str.replace(' name="' + str(var_from_target[_i]) + '"',
                                                ' name="' + soup_dom_concat + soup_dom_hex + '"')

            # 替换【config.xml】内的变量
            if os.path.exists(config_xml):
                config_soup_str = config_soup_str.replace('id="' + str(var_from_target[_i]) + '"',
                                                          'id="' + soup_dom_concat + soup_dom_hex + '"')

            # 替换【var_config.xml】内的变量
            if os.path.exists(var_config_xml):
                var_config_soup_str = var_config_soup_str.replace('name="' + str(var_from_target[_i]) + '"',
                                                                  'name="' + soup_dom_concat + soup_dom_hex + '"')

            # 替换【var_config.xml】内的变量
            if os.path.exists(var_config_xml):
                var_config_soup_str = var_config_soup_str.replace('repeatVar="' + str(var_from_target[_i]) + '"',
                                                                  'repeatVar="' + soup_dom_concat + soup_dom_hex + '"')

        # 保存【config.xml】
        if os.path.exists(config_xml):
            with open(config_xml, 'w', encoding='utf-8') as _f0:
                _f0.write(config_soup_str.replace('\n', ''))

        # 保存【var_config.xml】
        if os.path.exists(var_config_xml):
            with open(var_config_xml, 'w', encoding='utf-8') as _f0:
                _f0.write(var_config_soup_str.replace('\n', ''))

        if var_alias == 0:
            soup_dom_str = soup_dom_str.replace(manifest_root + ' ',
                                                manifest_root + ' _compiler_id="' + soup_dom_hex + '" ')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace(' target="' + str(var_from_target[_i]) + '"',
                                                ' target="' + soup_dom_concat + soup_dom_hex + '"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace(' dependency="' + str(var_from_target[_i]) + '"',
                                                ' dependency="' + soup_dom_concat + soup_dom_hex + '"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace(' indexName="' + str(var_from_target[_i]) + '"',
                                                ' indexName="' + soup_dom_concat + soup_dom_hex + '"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace(' countName="' + str(var_from_target[_i]) + '"',
                                                ' countName="' + soup_dom_concat + soup_dom_hex + '"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace(' src="' + str(var_from_target[_i]) + '.artwork"',
                                                ' src="' + soup_dom_concat + soup_dom_hex + '.artwork"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace(' strPara="\'' + str(var_from_target[_i]) + '\'"',
                                                ' strPara="\'' + soup_dom_concat + soup_dom_hex + '\'"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '"',
                                                '#' + soup_dom_concat + soup_dom_hex + '"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '"',
                                                '@' + soup_dom_concat + soup_dom_hex + '"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + ')',
                                                '#' + soup_dom_concat + soup_dom_hex + ')')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '+',
                                                '#' + soup_dom_concat + soup_dom_hex + '+')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '-',
                                                '#' + soup_dom_concat + soup_dom_hex + '-')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '*',
                                                '#' + soup_dom_concat + soup_dom_hex + '*')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '/',
                                                '#' + soup_dom_concat + soup_dom_hex + '/')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '%',
                                                '#' + soup_dom_concat + soup_dom_hex + '%')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '=',
                                                '#' + soup_dom_concat + soup_dom_hex + '=')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '=',
                                                '@' + soup_dom_concat + soup_dom_hex + '=')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '}',
                                                '#' + soup_dom_concat + soup_dom_hex + '}')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '}',
                                                '@' + soup_dom_concat + soup_dom_hex + '}')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '{',
                                                '#' + soup_dom_concat + soup_dom_hex + '{')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '{',
                                                '@' + soup_dom_concat + soup_dom_hex + '{')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '!',
                                                '#' + soup_dom_concat + soup_dom_hex + '!')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '!',
                                                '@' + soup_dom_concat + soup_dom_hex + '!')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '[',
                                                '#' + soup_dom_concat + soup_dom_hex + '[')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '[',
                                                '@' + soup_dom_concat + soup_dom_hex + '[')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('[#' + str(var_from_target[_i]) + ']',
                                                '[#' + soup_dom_concat + soup_dom_hex + ']')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('[@' + str(var_from_target[_i]) + ']',
                                                '[@' + soup_dom_concat + soup_dom_hex + ']')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + ',',
                                                '#' + soup_dom_concat + soup_dom_hex + ',')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + '.',
                                                '#' + soup_dom_concat + soup_dom_hex + '.')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[_i]) + ' ',
                                                '#' + soup_dom_concat + soup_dom_hex + ' ')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + ')',
                                                '@' + soup_dom_concat + soup_dom_hex + ')')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '+',
                                                '@' + soup_dom_concat + soup_dom_hex + '+')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + ',',
                                                '@' + soup_dom_concat + soup_dom_hex + ',')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + '.',
                                                '@' + soup_dom_concat + soup_dom_hex + '.')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[_i]) + ' ',
                                                '@' + soup_dom_concat + soup_dom_hex + ' ')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('src="' + str(var_from_target[_i]) + '"',
                                                'src="' + soup_dom_concat + soup_dom_hex + '"')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('"' + str(var_from_target[_i]) + '.animation',
                                                '"' + soup_dom_concat + soup_dom_hex + '.animation')

        for _i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[_i]) + '_'
            soup_dom_str = soup_dom_str.replace('"' + str(var_from_target[_i]) + '.visibility',
                                                '"' + soup_dom_concat + soup_dom_hex + '.visibility')

        # 删除无用的变量动画
        _soup_final = BeautifulSoup(soup_dom_str, features="lxml-xml")
        import copy
        _soup_final2 = copy.copy(_soup_final)
        for var_tag in _soup_final2.find_all('Var'):
            if var_tag.VariableAnimation:
                var_tag.decompose()
        _soup_temp = str(_soup_final2)
        # print(f'删除变量动画: {_soup_temp})

        _vars = []
        # 遍历Var标签
        for var_tag in _soup_final.find_all('Var'):
            if var_tag.VariableAnimation:
                var_name = '#' + str(var_tag.get('name'))
                var_name_e = str(var_tag.get('name'))
                # 排除默认动画变量 looping
                if var_tag.get('name') and var_tag.get('_glb') is None and str(alias_dict[var_name_e]) not in ['looping']:
                    var_content = str(var_tag)

                    if var_name in var_content and var_name not in _soup_temp:
                        _vars.append(var_name_e)
                    elif var_name in var_content and var_name in _soup_temp:
                        origin_var_e = alias_dict[var_name_e]
                        print(f"Exist: {{'{origin_var_e}': '{var_name_e}'}}")
                    elif var_name not in var_content and var_name not in _soup_temp:
                        _vars.append(var_name_e)

        # print(alias_dict)
        print('Decompose:')
        for _i in range(len(_vars)):
            origin_var = alias_dict[_vars[_i]]
            print(f"\t{{'{origin_var}': '{_vars[_i]}'}}")
        print('\t')

        # 查找变量动画，删除对应 AnimationCommand
        for _tags in _soup_final.find_all():
            if _tags.name == 'Var' and _tags.VariableAnimation and _tags.get('name'):
                var_name = _tags.get('name')
                for _i in range(len(_vars)):
                    if var_name == str(_vars[_i]):
                        _tags.decompose()
            if _tags.name == 'AnimationCommand' and _tags.get('target'):
                com_name = _tags.get('target')
                for _i in range(len(_vars)):
                    if com_name == str(_vars[_i]):
                        _tags.decompose()

        # 删除空闲 threshold
        for var in _soup_final.find_all('Var'):
            if var.get('threshold') is not None:
                var_contents = list(set(var.Trigger.contents))
                if var_contents == ['\n']:
                    var.decompose()

        for var_c in _soup_final.find_all('Trigger'):
            if var_c.parent.name == 'Var':
                for var_child in var_c.find_all('Var'):
                    # print(var_child)
                    var_child.decompose()

        # 删除 disabled != 0 的标签
        for _del_var in _soup_final.find_all('Var'):
            if _del_var.get('disabled') is not None:
                if _del_var.get('disabled') != '0':
                    _del_var.decompose()

        for _del_tag in _soup_final.find_all('Button'):
            if _del_tag.get('disabled') is not None:
                if _del_tag.get('disabled') != '0':
                    # print(_del_tag)
                    _del_tag.decompose()

        # 若变量动画 改变帧率控制器 自动获取最大时间
        if _soup_final.FramerateController:
            frame_control_time = [0, 100, 101]
            frame_time_collect = []
            for frame_control in _soup_final.find_all():
                if (frame_control.name == 'Item' or frame_control.name == 'AniFrame') and frame_control.get('time'):
                    frame_time_collect.append(frame_control.get('time'))
                    frame_time_collect.sort(key=lambda x: (int(x), x), reverse=True)

            for frame_control in _soup_final.find_all():
                if (frame_control.name == 'Item' or frame_control.name == 'AniFrame') and frame_control.get('time'):
                    frame_max_time = frame_time_collect[0]
                    frame_control_time[1] = int(frame_max_time)
                    frame_control_time[2] = int(frame_control_time[1] + 1)
                # 'VariableAnimation' not in _soup_final and
                if frame_control.name == 'FramerateController':
                    frame_control.contents = list(filter(lambda x: x != '\n', frame_control.contents))
                    control_point_num = len(frame_control.contents)
                    print(frame_time_collect)
                    print(frame_control_time)

            if control_point_num == 3:
                frame_controller = _soup_final.FramerateController
                frame_point = -1
                for frame_time in frame_controller:
                    frame_point += 1
                    frame_time['time'] = frame_control_time[frame_point]

        # 保存前的最后一步: 定义一个函数用于将中文和特殊字符转换为 Unicode 字符串
        unicode_mode = 1
        if unicode_mode:
            def convert_to_unicode(match):
                return '&#' + str(ord(match.group(0))) + ';'

            # 处理带有 format 和 text 属性的标签
            print('Unicode:')
            for var_tag in _soup_final.find_all():
                if '_ascii' not in var_tag.attrs and 'assigning' not in var_tag.attrs:
                    if 'format' in var_tag.attrs and all(
                            forbidden_char not in var_tag.get('format') for forbidden_char in "#@"):
                        format_value = var_tag['format']
                        format_unicode = re.sub(r'.', convert_to_unicode, format_value)
                        var_tag['format'] = format_unicode
                        print(f'\t{var_tag}')

                    if 'text' in var_tag.attrs and all(
                            forbidden_char not in var_tag.get('text') for forbidden_char in "#@"):
                        text_value = var_tag['text']
                        text_unicode = re.sub(r'.', convert_to_unicode, text_value)
                        var_tag['text'] = text_unicode
                        print(f'\t{var_tag}')

                    if 'value' in var_tag.attrs and var_tag.parent.name == 'Items' and all(
                            forbidden_char not in var_tag.get('value') for forbidden_char in "#@"):
                        text_value = var_tag['value']
                        text_unicode = re.sub(r'.', convert_to_unicode, text_value)
                        var_tag['value'] = text_unicode
                        print(f'\t{var_tag}')

                    for attrs in var_tag.attrs:
                        string_value = var_tag[attrs]
                        if '://' in str(string_value) and all(forbidden_char not in str(string_value) for forbidden_char in "#@"):
                            string_unicode = re.sub(r'.', convert_to_unicode, str(string_value))
                        else:
                            string_unicode = re.sub(r'[^\x00-\x7F]', convert_to_unicode, str(string_value))
                        var_tag[attrs] = string_unicode
                        # print(f'Unicode_CN: {var_tag.name}')
            print('\t')

        # 新增 src_exp_mode 将代码里的 srcid 写法转为 srcExp 写法（华为async模式）
        src_exp_mode = 1
        if src_exp_mode:
            print('srcExp:')
            for image in _soup_final.find_all():
                if image.get('src') and 'srcid' in image.attrs:
                    image_srcid = str(image.get('srcid'))
                    # print(image_srcid)
                    # and '%' not in image_srcid
                    if image_srcid.startswith('int(') or image_srcid.startswith('max('):
                        image_srcid_a = ''
                        image_srcid_b = ''
                    else:
                        image_srcid_a = 'int('
                        image_srcid_b = ')'
                    image_suffix = str(image.get('src')).split('.')[-1]
                    image_filename = str(image.get('src')).replace(f'.{image_suffix}', '')
                    image['srcExp'] = "'" + image_filename + "_'+" + image_srcid_a + image_srcid + image_srcid_b + "+'." + image_suffix + "'"
                    print(f"\t{image['srcExp']}")
                    del image['src']
                    del image['srcid']
            print('\t')

        soup_dom_str = str(_soup_final.prettify(indent_width=1))\
            .replace('    ', '\t').replace('&amp;#', '&#')\
            .replace('__widget_auto_size__', maml_folder_name.replace('widget_', ''))

        # # 删除 threshold 中的 Var 标签
        # for element in _soup_final.find_all():
        #     if element.name == 'Var' and element.parent.name == 'Trigger' and element.parent.parent.get('threshold') is not None:
        #         print(element)
        #         element.decompose()
        #         _soup_final = BeautifulSoup(str(_soup_final), 'lxml-xml')
        # print(_soup_final)
        # sys.exit(0)

        # print(soup_dom_str)

        # 检测/移除空属性
        for element in _soup_final.find_all():
            # 遍历元素的所有属性
            for attr_name, attr_value in element.attrs.items():
                if attr_value == '' or str(attr_value).strip() == '':
                    print(f'⚠️Warning: {element}')
                    time.sleep(1)

    with open(_success_xml, 'w', encoding='utf-8') as _f0:
        if var_alias:
            _f0.write(soup_dom_str.replace('\n', '').replace('&amp;#', '&#'))
        else:
            _f0.write(soup_dom_str.replace('&amp;#', '&#'))

    order_xml_mode = 1
    if order_xml_mode:
        import tools.order
        tools.order.orderXML(_success_xml)
    if var_get_source:
        import tools.anti
        tools.anti.convert_to_source(_anti_xml, _success_xml, _source_xml, 1, 0)

    # End

    if var_alias_anti == 1:

        var_from_target.sort(reverse=False)
        # print('var_from_target: ', var_from_target, '\n')
        alias_str = '<AntiAliasing version="1"></AntiAliasing>'
        _soup = BeautifulSoup(alias_str, features="lxml-xml")
        for alias in _soup.find_all('AntiAliasing'):
            for _j in range(len(var_from_target)):
                alias_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[_j]).encode('UTF-8')))[2:].capitalize()
                alias_dom_hex = 'm' if len(alias_dom_concat) == 8 else ''
                alias_str_new = _soup.new_tag('Aliasing', initial=str(var_from_target[_j]), after=str(alias_dom_concat + alias_dom_hex))
                alias.append(alias_str_new)

        with open(_anti_xml, 'w', encoding='utf-8') as _f0:
            _f0.write(str(_soup.prettify(indent_width=1)).replace('    ', '\t'))

    else:
        if os.path.exists(_anti_xml): os.remove(_anti_xml)

    if count <= 1 and var_alias_list == 1:

        alias_list = '<DisableAliasingList></DisableAliasingList>'
        _soup = BeautifulSoup(alias_list, features="lxml-xml")
        for anti_list in _soup.find_all('DisableAliasingList'):
            for alias_list in range(len(var_forbid_name)):
                alias_list_str = _soup.new_tag('DisableAliasing', attrs={'name': str(var_forbid_name[alias_list])})
                print(alias_list_str)
                anti_list.append(alias_list_str)
        with open(_anti_list_xml, 'w', encoding='utf-8') as _f0:
            _f0.write(str(_soup.prettify(indent_width=1)).replace('    ', '\t'))

    return


# 主程序
dirLib(lib_folder_name)
parseXML(maml_main_xml, parse_xml)
soup = BeautifulSoup(open(parse_xml, encoding="utf-8"), features="lxml-xml")

# 输出根标签
for root in soup.find_all(True, limit=1):
    manifest_root = str(root.name)
    manifest_sw = int(root.get('screenWidth'))
    manifest_sh = int(root.get('screenHeight', -1))

# globalPersist / _glb变量排除
for global_persist in soup.find_all(globalPersist=True, _glb=True):
    if global_persist.get('name') is not None:
        print(f"globalPersist: {global_persist['name']}")
        var_forbid_name.append(str(global_persist['name']))

# # globalPersist变量排除
# for global_persist in soup.find_all(globalPersist=True):
#     if global_persist.get('name') is not None:
#         print(f"globalPersist: {global_persist['name']}")
#         var_forbid_name.append(str(global_persist['name']))
#
# # _glb变量排除
# for global_persist in soup.find_all(_glb=True):
#     if global_persist.get('name') is not None:
#         print(f"globalPersist: {global_persist['name']}")
#         var_forbid_name.append(str(global_persist['name']))

# <Import name="mGlobalVar" globalPersist="true" />

# 输出除Lockscreen外的所有标签 
# re.compile("^(?!.*Lockscreen)^(?!.*Widget)^(?!.*Icon)")

# 将 SysTime 标签前置
# for _sys in soup.find_all('SysTime'):
#     # print(_sys.name)
#     new_sys_time = _sys
#     _sys.extract()
#
# if soup.find_all('SysTime'):
#     for _r in soup.find_all(True, limit=2):
#         if _r.name != manifest_root:
#             _r.insert_before(new_sys_time)
#             print(soup)
#             soup = BeautifulSoup(str(soup), 'lxml-xml')

print('Disabled:')

# Main / Start
for tag in soup.find_all(True):

    # 匹配库文件标签

    for i in range(len(lib)):

        if tag.name == lib[i] and tag.get('card') != 'Almanac' and tag.get('card') != 'Constellations' and tag.get(
                'card') != 'BigEvent':

            # 检测【disabled】属性是否存在，若存在则删除标签，并重新写入soup

            if tag.get('disabled') is not None and tag.get('disabled') != '0':

                print(f'\t{tag}')
                tag.decompose()

                with open(parse_xml, 'w', encoding='utf-8') as f0:
                    f0.write(str(soup))

            else:
                tags_lib.append(tag.name)
                tags_str.append(str(tag))

                # 检测库标签是否有[tag_keys]属性，如有则不给变量加随机值后缀

                tags_port = str(tag.get('_port'))
                if tags_port == 'None':
                    tags_port = str(tag.get('_importlib'))
                    if tags_port == 'None':
                        tags_port = str(tag.get('_globalport'))
                        if tags_port == 'None':
                            tags_port = str(tag.get('_newport'))
                if tags_port != 'None':
                    var_alias_all = 0
                else:
                    var_alias_all = 1

                if len(tags_lib) > 0:

                    # 获取库文件Attributes以及相应默认值

                    lib_soup_attr.clear()
                    lib_soup_attr_def.clear()
                    tags_attr.clear()

                    # print(lib[i], 'Here')
                    getLib(lib[i])
                    # lib_valueholder_num = len(lib_valueholder)
                    # print('lib_valueholder: ', lib_valueholder, '\n')

                    # 获取本地Slot标签
                    if tag.Slot is None:
                        new_tag_count = 0
                        while new_tag_count < lib_slots_num[lib[i]]:
                            new_tag_slot = soup.new_tag('Slot', id=randomHex(8))
                            new_tag_slot.string = '<!-- ' + 'Slot.id=\"' + new_tag_slot.get('id') + '\" -->'
                            tag.append(new_tag_slot)
                            tags_slots.append(new_tag_slot.string)
                            new_tag_count = new_tag_count + 1
                    else:
                        # 将Slot标签内的变量名改为全局变量，避免加后缀
                        for t in tag.find_all('Slot'):

                            for u in t.find_all(name=True):
                                if u.get('name') is not None:
                                    u['name'] = '$' + u.get('name') + '$'

                            for u in t.find_all(indexName=True):
                                if u.get('indexName') is not None:
                                    u['indexName'] = '$' + u.get('indexName') + '$'

                            for u in t.find_all(countName=True):
                                if u.get('countName') is not None:
                                    u['countName'] = '$' + u.get('countName') + '$'

                            for u in t.find_all(target=True):
                                if u.get('target') is not None:
                                    # if '.visibility' in u.get('target'):
                                    # u['target'] = '$' + str(u.get('target')).replace('.visibility') + '$'
                                    u['target'] = '$' + u.get('target') + '$'

                        for t in tag.find_all('Slot'):
                            for k in t.find_all(True):
                                tags_slots.append(str(k))

                    # 获取本地Attributes
                    if lib_valueholder_num == 0:
                        for j in range(len(lib_soup_attr)):
                            tags_attr.append(tag.get(lib_soup_attr[j]))
                    else:
                        for k in tag.find_all('ValueHolder'):
                            h = k['value']
                            tags_attr.append(str(h))

                    if len(lib_placeholder_attr):
                        lib_placeholder_to_string = ''
                        for p in tag.find_all(True):
                            for q in range(len(lib_placeholder_attr)):
                                if p.name == lib_placeholder_attr[q]:
                                    # for n in range(len(p.contents)):
                                    for s in range(len(p.contents)):
                                        lib_placeholder_to_string = lib_placeholder_to_string + str(p.contents[s])
                                    # print(lib_placeholder_to_string, '\n')
                                    # lib_placeholder_to_string = p.find_all(True)
                                    lib_placeholder_str2.append(lib_placeholder_to_string)
                                # print('lib_placeholder_to_string: ', lib_placeholder_to_string)

                    # 获取库文件主内容并替换Attributes
                    if lib[i] == 'InputDate' and tag.get('_id') is not None:
                        lib_dom_id = 1
                        # _port
                        var_alias_all = 1
                        lib_dom_input = tag.get('_id')
                    else:
                        var_alias_all = 0
                        lib_dom_id = 0
                        lib_dom_input = None

                    getLibContent(lib[i], lib_dom_id, lib_dom_input)

                # print('l_lib: ',len(lib_slots))
                # print('l_tags: ',len(tags_slots), '\n')
                # print('lib_slots: ', lib_slots, '\n')
                # print('tags_slots: ', tags_slots, '\n')

# 重新解析XML
soup = BeautifulSoup(open(parse_xml, encoding="utf-8"), features="lxml-xml")
for name_exp in soup.find_all(nameExp=True):
    print(f"nameExp[{randomHex(8)}]: {str(name_exp)}")
dev_time = getTimeSys()
soup_indent = str(soup)
# print('soup: ', soup)

with open(parse_xml, 'w', encoding='utf-8') as f0:
    f0.write(soup_indent)

with open(parse_xml, 'r', encoding='utf-8') as f:
    with open(success_xml, 'w', encoding='utf-8') as f2:
        for line in f:
            for k in range(len(tags_str)):
                # 本地替换为库
                # print(tags_str)
                # print(lib_soup_str)
                line = line.replace(str(tags_str[k]), str(lib_soup_str[k]))
            f2.write(line)

saveXML(success_xml)

# 复制代码库对应图片素材

# 遍历每个lib文件夹
for lib_folder in tags_lib:
    src_folder = os.path.join(lib_folder_name, lib_folder)
    dst_folder = os.path.join(assets_folder_name, lib_folder)

    # 创建目标文件夹
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    # 遍历源文件夹的每个子文件夹和文件
    for root, dirs, files in os.walk(src_folder):
        # 排除preview文件夹和xml文件
        if os.path.basename(root) == 'preview' or os.path.splitext(root)[1] == '.xml':
            continue

        # 复制子文件夹
        for d in dirs:
            src_subfolder = os.path.join(root, d)
            if not src_subfolder.endswith('preview'):
                dst_subfolder = os.path.join(dst_folder, os.path.relpath(src_subfolder, src_folder))
                if not os.path.exists(dst_subfolder):
                    os.makedirs(dst_subfolder)

        # 复制文件
        for f in files:
            src_file = os.path.join(root, f)
            if not src_file.endswith('.xml'):
                dst_file = os.path.join(dst_folder, os.path.relpath(src_file, src_folder))
                shutil.copy(src_file, dst_file)

removeEmpty(os.path.join(os.getcwd(), assets_folder_name))
cleanCache()
getAlias()

# print('lib: ',lib, '\n')
# print('tags_lib: ',tags_lib, '\n')
# print('tags_str: ',tags_str, '\n')
# print('tags_attr: ',tags_attr, '\n')
# print('lib_soup_attr: ',lib_soup_attr, '\n')
# print('lib_soup_attr_def: ',lib_soup_attr_def, '\n')
# print('lib_soup_str: ',lib_soup_str, '\n')


def compressMAML():

    # 读取 XML 文件
    with open(maml_main_xml, "rb") as file:
        xml_string = file.read()

    # 解析 XML
    _soup = BeautifulSoup(xml_string, "xml")

    # 查找并删除带有 disabled 属性且值不为0的标签
    for element in _soup.find_all(attrs={"disabled": lambda x: x and x != "0"}):
        element.extract()

    # 获取更新后的 XML 字符串
    updated_xml = str(_soup)

    # 计算字符串的大小（KB）
    size_in_kb = len(updated_xml.encode("utf-8")) / 1024

    # 打印删除后的 XML 大小
    # print(f"删除后的 XML 大小：{size_in_kb:.2f} KB")

    return size_in_kb


def calculateMemory(folder_path=None):
    from PIL import Image

    if folder_path is None:
        folder_path = pyperclip.paste()

    folder_path_abs = folder_path.replace(maml_rule_file, '')
    folder_path = os.path.dirname(folder_path)

    total_memory = 0
    image_compress_ratio = 720 / 1080
    image_compress_mode = 0

    print(f'CompressMode: {image_compress_mode}')
    for _root, _, _files in os.walk(folder_path):
        if len(_files) <= 1000:
            for filename in _files:
                _file_path = os.path.join(_root, filename)
                if filename.startswith("._") or filename == ".DS_Store":
                    try:
                        os.remove(_file_path)
                        print(f'Remove: {filename}')
                    except Exception as _file_e:
                        print(f"Exception: {_file_e}")

                if any(_file_path.endswith(ext) for ext in ['.xml', '.mp3', '.mp4']):
                    continue  # 检查文件扩展名是否为.xml .mp3 .mp4 跳过
                try:
                    image = Image.open(_file_path)
                    width, height = image.size
                    memory_mb = width * height * 4 / (1024 * 1024)
                    # print(_file_path)
                    # (width >= 1080 and height >= 960) or (width >= 540 and height >= 1200):

                    if not any(os.path.basename(_file_path) == ext for ext in ['bg.png', 'statusbar.png']):
                        if memory_mb >= 3 and width > 720:
                            print(f"Oversize: {width} x {height}, {_file_path.replace(folder_path_abs, '')}, {memory_mb} MB")
                            _file_path_abs = _file_path.replace(folder_path_abs, '')
                            # if (os.path.dirname(_file_path).endswith('assets') or os.path.dirname(_file_path).endswith('a') or os.path.dirname(_file_path).endswith('b')) \
                            if (_file_path_abs.startswith('assets') or _file_path_abs.startswith('bz')) and image_compress_mode:
                                new_width = int(width * image_compress_ratio)
                                new_height = int(height * image_compress_ratio)
                                resized_image = image.resize((new_width, new_height))
                                resized_image.save(_file_path)
                                print(f"Compressed: {new_width} x {new_height}, {_file_path_abs}, {memory_mb} MB")
                                # image.size = width * image_compress_ratio, height * image_compress_ratio
                                # image.save(_file_path)
                                width = new_width
                                height = new_height

                    memory = width * height * 4  # 假设每个像素占用4字节内存
                    total_memory += memory
                    image.close()
                # except:
                except Exception as memory_e:
                    print(f"Exception: {memory_e}")

    # 压缩文件夹并获取压缩文件大小
    zip_path = folder_path + '.zip'
    shutil.make_archive(folder_path, 'zip', folder_path)
    zip_size = os.path.getsize(zip_path)
    zip_size_mb = zip_size / (1024 * 1024)  # 转换为MB
    os.remove(zip_path)  # 删除临时的压缩文件

    print('\t')
    print(f"Package: {zip_size_mb:.2f} MB | 10.24 MB")  # 输出文件夹压缩后的占用大小，单位为MB
    # print(f"Memory: {total_memory} bytes")  # 输出总内存占用，单位为字节
    # print(f"Memory: {total_memory / (1024 * 1024):.2f} MB ~ {2 * total_memory / (1024 * 1024):.2f} MB | 600.00 MB")  # 输出总内存占用，单位为MB
    strict_mode = 1
    total_memory_unit = 1 if strict_mode else 0.88230
    total_memory_heytap = 2 * total_memory / (1024 * 1024)
    total_memory_harmony = (6 + 128 + total_memory_heytap)
    total_memory_origin = total_memory_unit * (total_memory_harmony - 128 - 6)
    print(f"Memory: {total_memory_origin * 1024 :.0f} KB | 614400 KB")  # 输出总内存占用
    print('\t')

    return total_memory


def applyTestClass(xml_file_path):
    def compress_folder_as_mtz(_input_folder):
        # 获取传入文件夹的名称
        base_folder_name = os.path.basename(_input_folder)
        output_file_name = f"{base_folder_name}.mtz"

        # 创建一个临时文件夹，用于存放模块和wallpaper、pictures文件夹
        temp_folder = os.path.join(os.path.dirname(_input_folder), "temp_folder")
        os.makedirs(temp_folder, exist_ok=True)

        # 遍历传入文件夹下的子文件夹和文件
        for item in os.listdir(_input_folder):
            item_path = os.path.join(_input_folder, item)

            # 如果是文件夹，则判断是否是wallpaper或pictures文件夹
            if os.path.isdir(item_path):
                if item in ["wallpaper", "pictures", "compatibility-v12"]:
                    # 直接将wallpaper和pictures文件夹拷贝到临时文件夹
                    shutil.copytree(item_path, os.path.join(temp_folder, item))
                else:
                    # 压缩子文件夹为模块
                    module_name = item
                    zip_file_name = os.path.join(temp_folder, f"{module_name}")
                    shutil.make_archive(zip_file_name, 'zip', item_path)
                    os.rename(zip_file_name + '.zip', os.path.join(temp_folder, module_name))
            else:
                # 如果是普通文件，则直接拷贝到临时文件夹
                shutil.copy(item_path, temp_folder)

        # 压缩临时文件夹为mtz文件
        shutil.make_archive(os.path.join(os.path.dirname(_input_folder), base_folder_name), 'zip', temp_folder)

        # 删除临时文件夹
        shutil.rmtree(temp_folder)

        # 重命名生成的zip文件为.mtz
        os.rename(f"{os.path.join(os.path.dirname(_input_folder), base_folder_name)}.zip", os.path.join(os.path.dirname(_input_folder), output_file_name))

        # 转义空格目录 兼容T7/Users/wangshilong/Desktop/导出/待办/麦禾-木兰/！165.油画风维尼小伙伴锁屏说明_1837274363/国内版/OPPO/lockscreen/advance/maml.xml
        _mtz_file_path = os.path.join(os.path.dirname(_input_folder), output_file_name).replace(" ", "' '")

        return _mtz_file_path

    def apply_theme_class(mtz_file_path, ip_address="192.168.31.244"):
        # mtz_file_target = '/sdcard/tmp.mtz'
        mtz_file_target = '/sdcard/Android/data/com.android.thememanager/files/snapshot/tmp.mtz'

        # 定义变量，用于存储 *.mtz 文件的路径

        # 命令0: adb devices
        devices_command = f"adb devices"

        # 命令1: adb connect
        if not connected:
            connect_command = f"adb connect {ip_address}"

        # 命令2: adb push
        push_command = f"adb push {mtz_file_path} {mtz_file_target}"

        # 命令3: adb shell am start
        start_command = "adb shell am start -n com.android.thememanager/.ApplyThemeForScreenshot " \
                        f"--es theme_file_path '{mtz_file_target}' --es api_called_from 'Xiaomi-Theme'"

        # 命令4: adb shell wm size
        resize_command = f"adb shell wm size {manifest_sw}x{manifest_sh}"

        try:
            # 执行命令0: adb devices
            devices_result = subprocess.run(devices_command, shell=True, capture_output=True, text=True)
            print(devices_result.stdout)

            # 执行命令1: adb connect
            if not connected:
                connect_result = subprocess.run(connect_command, shell=True, capture_output=True, text=True)
                print(connect_result.stdout)

            # 执行命令2: adb push
            push_result = subprocess.run(push_command, shell=True, capture_output=True, text=True)
            print(push_result.stdout)

            # 执行命令3: adb shell am start
            start_result = subprocess.run(start_command, shell=True, capture_output=True, text=True)
            print(start_result.stdout)

            if manifest_sh:
                # 执行命令4: adb shell wm size
                resize_result = subprocess.run(resize_command, shell=True, capture_output=True, text=True)
                print(resize_result.stdout)

        except Exception as apply_e:
            print(f"Error: {apply_e} - apply_theme_class()")

    if __name__ == "__main__":
        print("{:-^42s}\n".format(" Android Debug Bridge "))
        # input_folder = "/Users/wangshilong/Desktop/导出/asar/FFF/lockscreen/advance/maml.xml"  # 替换为您的输入文件夹路径
        input_folder = xml_file_path.replace(f'/lockscreen/advance/{maml_rule_file}', '')
        compress_folder_as_mtz(input_folder)
        mtz_file = compress_folder_as_mtz(input_folder)
        apply_theme_class(mtz_file, ip_address_arr[ip_address_id])


end_time = time.time()  # 记录结束时间
run_time = f'{(end_time - start_time):.2f}'  # 计算运行时间
local_xml = os.path.abspath(sys.argv[0]).replace('main.py', maml_rule_file)

# calculateMemory and applyTestClass

if 'PYCHARM_HOSTED' in os.environ and maml_main_xml != local_xml and maml_folder_name == 'advance':
    calculateMemory()
    apply_test = 1
    ip_address_id = 4 if wifi_in_vgoing else 0
    # 0:K40S  1:K20Pro 2:Hotpot K40S 3:Hotpot K20Pro
    ip_address_arr = ('192.168.31.241', '192.168.31.201', '172.20.10.2', '172.20.10.8', '192.168.0.216')
    if manifest_root == 'Lockscreen' and wifi_state and apply_test:

        connected = 1
        # connected 1:USB连接 0:Wi-Fi连接
        try:
            print(f'Connect: {connected}')
            applyTestClass(maml_main_xml)
        except Exception as e:
            print(f"Error: {e}")

# calculateCompressRate

maml_size = compressMAML()
manifest_size = os.path.getsize(success_xml) / 1024  # 转换为KB
compress_rate = f'{(maml_size / manifest_size * 100):.2f}%'
print(f"Done, Script Run Time: {run_time}秒, CompressRate: {compress_rate}")
log_message = f"Script Run Time: {run_time} seconds, <CompressRate value=\"{compress_rate}\" count=\"{count}\" dev_time=\"{dev_time}\" />"
logging.info(log_message)

# 连接到数据库
conn = sqlite3.connect(os.path.join(database_path, "counter.db"))
conn.execute("INSERT INTO counter (count, source, compress_rate, run_time, dev_time) VALUES (?, ?, ?, ?, ?)",
             (count, maml_main_xml, compress_rate, run_time, dev_time))
conn.commit()
# 关闭数据库连接
conn.close()
# time.sleep(2)
sys.exit(0)
