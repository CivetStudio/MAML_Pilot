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
01.08 splitTools.py 自动修复不带【name】属性的【threshold】/【*Animation】标签
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

    TODO*: 1.当缺少 ['w', 'h'] 属性时，能否从文件路径中寻找对应值（考虑srcid, srcExp）
    07.12 新增支持 Rectangle 标签
02.02 新增 C_Array 数组标签写法: 支持单条的 VariableCommand 命令（不可与其他标签共用）
    <C_Array count="4" indexName="index">
        <VariableCommand name="test_#index" expression="#index" type="number" />
    </C_Array>
    16:18 已修复为自动识别代码，支持解析 {$pattern$} 为 eval($pattern$)
    TODO: C_Array 解析 Group 标签时多次复制
02.21 新增 SoundCommand 自动处理：带 condition 属性的 SoundCommand 标签单独处理
	2024.07.10 新增 _condition 属性存在时，屏蔽处理（适用于华为）
03.15 重构加解密代码 -> dev.Refactor.refactor
03.20 数据库新增列 anti_json 负责记录 var_alias_dict
03.21 代码中新增变量 Key 作为解密（AES-256），Key['expression'] = encrypt_text(anti_json) 即 var_alias_dict 的加密版本
04.02 新增 globalPersist 自动删除规则：
    若 Var['globalPersist'] == 'true':
        del VariableCommand[name='{Var['name']}'].get('persist')
04.08 新增 C_Array 标签支持数组变量: (建议于 C_Array 标签内调用，否则可能误删小米)
    type="number[]" 数字类型数组
    type="string[]" 文本类型数组
    使用时 Var 需加上 _c="1"，与 MIUI 分辨
BETA_04.13 （已移除）新增 属性解析 eval 功能：（与 C_Array 的解析方式一致，支持常数变量解析）
    # eval {eval_content} eg: "{0+1}" => "1"
    from tools.arrayc import eval_soup
    complex from refactor.py
    04.14 新增 eval_all_mode：若预览器需要改变量的值，不需要开启，主要用于刷新代码内所有常数
BETA_04.27 新增 解析函数功能：parse_function_beta
    当 count 参数缺失时：当作 Slot 使用，可省略 params 参数
    否则： count 与 params 为必填项，且 count 与 params 内的数量必须一致

    07.12 Support ['condition'] attribution (Only for '*Command' Tags)

    # 用法示例：
    <Fun name="Demo1" count="3" >
        <VariableCommand name="{param1}" expression="{param2}" type="number" />
        <VariableCommand name="{param3}" expression="{param4}" type="number" />
    </Fun>
    <FunCom condition="1" target="Demo1" params="{'param1': 'test_0', 'param2': '2', 'param3': 'test_1', 'param4': '4'}" />
05.12 新增 ValueHolder['default'] 默认值定义:
    # 用法示例
    <ValueHolder name="CalendarRotation" default="0" />
    目前 ValueHolder 可自动获取默认值，以便后期新增属性
05.30 新增 modules/Demo/manifest.xml 写法 V2:
    https://zhuti.designer.xiaomi.com/docs/blog/modular.html
06.04 新增 OPPO 组件卡加入合并 InputGroup 标签
06.20 优化 VarArray 检测逻辑
BETA_07.10 通过获取 VariableCommand 删除无用的变量
BETA_07.12 通过获取 Button 的 align、alignV 属性，自动修改坐标值
07.12 修复 '&lt;'/'&gt;' 转码失败

⚠️TODO: START
a. 检测图片是否在代码内：
    1. "pic.png": search directly
    2. if "_" in "pic_0.png":
        prefix = split("_")[0] = "pic"
        and search "pic.png" or "pic_" in code

b. Soft 检测 IntentCommand 中 package 与 class 是否都存在（VIEW除外）
c. Soft 需求：【Mask / Paint / LrcView】从Group中提取

遗留问题: 四个空格转为/t
⚠️TODO: END
"""


import platform
import warnings
import logging
import os
import re
import sys
import shutil
import sqlite3
import time
import zlib
import pyperclip
import subprocess
from bs4 import BeautifulSoup, Comment

import dev.Refactor.refactor
from dev.Refactor.refactor import aes_decode
from dev.Refactor.refactor import aes_encode
# import wx
# import requests

# from splitTools import splitVar, splitExt, splitBinders, splitGroup, preLoadVar, preLoadExt, intentMarket
from splitTools import *
from dev.Refactor.refactor import *
from dev.Refactor.Var.var_forbid import var_forbid_name as vfb
var_forbid_name = vfb


# 禁用特定警告
warnings.filterwarnings("ignore", category=UserWarning, message=".*MarkupResemblesLocatorWarning.*")
warnings.simplefilter("ignore", category=UserWarning)

RELEASE = 0

sys_version = 0
current_dir = os.getcwd()
maml_main_xml = str(pyperclip.paste()).replace('\\', '/').replace('"', '')
maml_rule_file = "maml"
maml_file_name = os.path.basename(maml_main_xml)
maml_folder_name = os.path.dirname(maml_main_xml).split('/')[-1]

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
modules_folder_name = os.path.join(current_dir, 'modules')
assets_folder_name = os.path.join(current_dir, 'assets')

# 创建lib文件夹
if not os.path.exists(lib_folder_name):
    os.makedirs(lib_folder_name)

# 创建modules文件夹
if not os.path.exists(modules_folder_name):
    os.makedirs(modules_folder_name)

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
             dev_time TEXT,
             anti_json TEXT
             );''')
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
# var_forbid_name = ['Almanac', 'Almanac.baiji', 'Almanac.caishen', 'Almanac.chenA', 'Almanac.chenB', 'Almanac.chongsha',
#                    'Almanac.chouA', 'Almanac.chouB', 'Almanac.fushen', 'Almanac.ganzhi', 'Almanac.haiA', 'Almanac.haiB',
#                    'Almanac.ji', 'Almanac.jishen', 'Almanac.maoA', 'Almanac.maoB', 'Almanac.nongli', 'Almanac.riwuxing',
#                    'Almanac.shen12', 'Almanac.shenA', 'Almanac.shenB', 'Almanac.shengxiao', 'Almanac.siA',
#                    'Almanac.siB', 'Almanac.taishen', 'Almanac.weiA', 'Almanac.weiB', 'Almanac.wuA', 'Almanac.wuB',
#                    'Almanac.xingxiu28', 'Almanac.xiongshen', 'Almanac.xishen', 'Almanac.xuA', 'Almanac.xuB',
#                    'Almanac.yangli', 'Almanac.yi', 'Almanac.yinA', 'Almanac.yinB', 'Almanac.yingui', 'Almanac.youA',
#                    'Almanac.youB', 'Almanac.zhishen', 'Almanac.ziA', 'Almanac.ziB', 'BigEvent_0', 'BigEvent_0.event',
#                    'BigEvent_0.year', 'BigEvent_1', 'BigEvent_1.event', 'BigEvent_1.year', 'BigEvent_2',
#                    'BigEvent_2.event', 'BigEvent_2.year', 'BigEvent_3', 'BigEvent_3.event', 'BigEvent_3.year',
#                    'BigEvent_4', 'BigEvent_4.event', 'BigEvent_4.year', 'ChargeSpeed', 'ChargeWireState',
#                    'Constellations', 'Constellations.signName', 'Constellations.today.datetime',
#                    'Constellations.today.healthStar', 'Constellations.today.loveDes', 'Constellations.today.loveStar',
#                    'Constellations.today.luckyColor', 'Constellations.today.luckyNumber',
#                    'Constellations.today.matchSign', 'Constellations.today.moneyDes', 'Constellations.today.moneyStar',
#                    'Constellations.today.summaryDes', 'Constellations.today.summaryStar',
#                    'Constellations.today.workDes', 'Constellations.today.workStar', 'MiStep', 'MiSteps',
#                    'MiSteps_distance', 'MiSteps_energy', 'MiSteps_goal', 'MiSteps_steps', 'MiSteps_strength_duration',
#                    'MiSteps_summary', 'Mi_begin_time', 'Mi_end_time', 'Mi_step', 'Progress', 'SetLanguage', 'Weather',
#                    'Weather.today.aqivalue', 'Weather.today.aqivaluetext', 'Weather.today.carWashLevel',
#                    'Weather.today.cnweatherDes', 'Weather.today.cnweatherid', 'Weather.today.coldLevel',
#                    'Weather.today.currentTem', 'Weather.today.dressingLevel', 'Weather.today.humidity',
#                    'Weather.today.maxtemp', 'Weather.today.mintemp', 'Weather.today.moonRise', 'Weather.today.moonSet',
#                    'Weather.today.sportsLevel', 'Weather.today.sunRise', 'Weather.today.sunSet',
#                    'Weather.today.weatherDes', 'Weather.today.weatherIcon', 'Weather.today.weatherIconDes',
#                    'Weather.today.weatherid', 'Weather.today.winddir', 'Weather.today.winddirDes',
#                    'Weather.tomorrow.aqivalue', 'Weather.tomorrow.aqivaluetext', 'Weather.tomorrow.carWashLevel',
#                    'Weather.tomorrow.cnweatherDes', 'Weather.tomorrow.cnweatherid', 'Weather.tomorrow.coldLevel',
#                    'Weather.tomorrow.currentTem', 'Weather.tomorrow.dressingLevel', 'Weather.tomorrow.humidity',
#                    'Weather.tomorrow.maxtemp', 'Weather.tomorrow.mintemp', 'Weather.tomorrow.moonRise',
#                    'Weather.tomorrow.moonSet', 'Weather.tomorrow.sportsLevel', 'Weather.tomorrow.sunRise',
#                    'Weather.tomorrow.sunSet', 'Weather.tomorrow.weatherDes', 'Weather.tomorrow.weatherIcon',
#                    'Weather.tomorrow.weatherIconDes', 'Weather.tomorrow.weatherid', 'Weather.tomorrow.winddir',
#                    'Weather.tomorrow.winddirDes', 'Weather.yesterday.aqivalue', 'Weather.yesterday.aqivaluetext',
#                    'Weather.yesterday.carWashLevel', 'Weather.yesterday.cnweatherDes', 'Weather.yesterday.cnweatherid',
#                    'Weather.yesterday.coldLevel', 'Weather.yesterday.currentTem', 'Weather.yesterday.dressingLevel',
#                    'Weather.yesterday.humidity', 'Weather.yesterday.maxtemp', 'Weather.yesterday.mintemp',
#                    'Weather.yesterday.moonRise', 'Weather.yesterday.moonSet', 'Weather.yesterday.sportsLevel',
#                    'Weather.yesterday.sunRise', 'Weather.yesterday.sunSet', 'Weather.yesterday.weatherDes',
#                    'Weather.yesterday.weatherIcon', 'Weather.yesterday.weatherIconDes', 'Weather.yesterday.weatherid',
#                    'Weather.yesterday.winddir', 'Weather.yesterday.winddirDes', '__android_version', 'night_mode',
#                    'darkMode', '__darkmode', '__darkmode_wallpaper', '__maml_version', '__miui_version_code',
#                    '__miui_version_name', '__thememanager_version', 'almanacRespCode', 'ampm',
#                    'applied_light_wallpaper', 'aqi_level', 'automaticRotary', 'automaticRotaryValue', 'battery_level',
#                    'battery_state', 'bigEventRespCode', 'call_missed_count', 'calories_value', 'cityid', 'cityname',
#                    'cityname_en', 'cityname_tw', 'clock_button', 'constellationRespCode', 'constellationsId',
#                    'cur_aqi_co', 'cur_aqi_level', 'cur_aqi_no', 'cur_aqi_no2', 'cur_aqi_o3', 'cur_aqi_so',
#                    'cur_avg_aqi', 'cur_avg_pm25', 'cur_pm10', 'cur_pressure', 'cur_uv_desc', 'cur_uv_index',
#                    'cur_visibility', 'cur_weather', 'cur_weather_direct', 'cur_weather_humidity', 'cur_weather_power',
#                    'cur_weather_temp', 'cur_weather_type', 'date', 'date_lunar', 'day_temp', 'day_weather_type',
#                    'defaultScreen_x', 'defaultScreen_y', 'deviceTime', 'distance_value', 'feast', 'festival',
#                    'flashlight', 'flashlightValue', 'face_enable', 'face_detect_state_msg', 'face_detect_help_msg',
#                    'fod_enable', 'fod_height', 'fod_state_msg', 'fod_width', 'fod_x', 'fod_y', 'frame_rate',
#                    'hasSteps', 'hasWeather', 'hassteps', 'health1', 'heart_rate_value', 'hour', 'hour12', 'hour24',
#                    'isPreviewMode', 'isMatePad_H_2560', 'isMatePad_V_1600', 'isSupportMicro',
#                    'is_music_playing', 'is_work_day', 'ishour12', 'lunarDay', 'lunarMonth', 'lunarYear',
#                    'lunar_solar_term', 'mCivetCode_000', 'mCivetCode_001', 'mCivetCode_002',
#                    'mCivetCode_003', 'mCivetCode_004', 'mCivetCode_005', 'mCivetCode_006', 'mCivetCode_007',
#                    'mCivetCode_008', 'mCivetCode_009', 'mCivetCode_010', 'mGlobalVar', 'mGlobalVar_2H', 'media_genres',
#                    'media_like_status', 'media_loading_status', 'media_mode_status', 'media_play_status',
#                    'media_subtitle', 'media_title', 'microPhone_state', 'microPhone_volume', 'microphone_state',
#                    'minute', 'month', 'month1', 'month_lunar', 'month_lunar_leap', 'musicPlayDuration',
#                    'musicPlaySecond',
#                    'musicTotalDuration', 'musicTotalSecond', 'music_active', 'music_album_cover', 'music_control',
#                    'music_display', 'music_next', 'music_pause', 'music_play', 'music_prev', 'next_alarm_time',
#                    'night_temp', 'night_weather_type', 'noticeDown', 'notification', 'ownerinfo', 'point_count',
#                    'pollingTime', 'processCpuFree', 'processCpuRate', 'rain_probability', 'raw_screen_height',
#                    'raw_screen_width', 'real_feel_temp', 'repeat_mode', 'resting_heart_rate_value', 'screen_density',
#                    'second', 'shake', 'shake_record', 'x_acc', 'y_acc', 'z_acc',
#                    'sms_unread_count', 'sport_value', 'step', 'step_today', 'steps_value',
#                    'storageFree', 'storageFreeNum', 'storageTotal', 'storageTotalNum', 'sunrise_time', 'sunset_time',
#                    'system.date', 'system.time.ampm', 'system.time.hour1', 'system.time.hour2', 'system.time.min1',
#                    'system.time.min2', 'systemVersion', 'time', 'timeZone', 'time_format', 'time_sys',
#                    'touch_begin_time', 'touch_begin_x', 'touch_begin_y', 'touch_pressure', 'touch_x', 'touch_y',
#                    'vibration', 'view_height', 'view_width', 'volume_level', 'volume_level_old', 'volume_type',
#                    'weather', 'weather1', 'weather2', 'weather3', 'weatherRespCode', 'weather_', 'weather_city',
#                    'weather_condition', 'weather_cur_temp', 'weather_description', 'weather_high_temp', 'weather_id',
#                    'weather_location', 'weather_low_temp', 'weather_publish_time', 'weather_sunrise', 'weather_sunset',
#                    'weather_temperature', 'weather_tmphighs', 'weather_tmplows', 'weather_wind_dir', 'weather_wind_pow',
#                    'year_lunar', 'year_lunar1864', 'year_lunar_leap', 'lunar_calendar_enable', 'battery_enable',
#                    'notification_enable', 'preview_mode', 'connectedStatus', 'headsetName', 'headsetBatteryLevel',
#                    'in_preview_mode']


var_alias_list = 1
var_alias_anti = 1

lib_slot_xml = "$.dll"
process_xml = "$0.dll"
parse_xml = "$1.dll"
success_xml = maml_main_xml.replace(maml_rule_file, 'manifest')
anti_xml = "antiAliasing.xml"
config_xml = maml_main_xml.replace(maml_rule_file, 'config')
var_config_xml = maml_main_xml.replace(maml_rule_file, 'var_config')
# var_config_xml = "var_config.xml"

# langs_id = 0
langs_id = 4 if os.path.exists(config_xml) or os.path.exists(var_config_xml) else 2
var_persist_attr = "const" if langs_id == 0 or langs_id == 4 else "persist"


# 获取网络时间戳
def getTimeSys():
    def get_wifi_ssid():
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

    global wifi_state
    global wifi_in_vgoing

    wifi_ssid = get_wifi_ssid()
    wifi_state = wifi_ssid in ["Redmi_71E5", "Civet's iPhone", "Xiaomi_4A3E", "vgoing"]
    wifi_in_vgoing = wifi_ssid == "vgoing"

    # print(wifi_state)

    timestamp_ms = int(time.time() * 1000)
    return timestamp_ms


def cleanComments(soup):
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    return soup


# 清理缓存文件
def cleanCacheBefore():
    if os.path.exists(anti_xml):
        os.remove(anti_xml)


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
    return lib


def getLibFile(lib_file, _mode=0, plugin_src='.'):
    if _mode <= 1:
        if os.path.exists('' + lib_folder_name + '/' + lib_file + '/' + lib_file + '.xml'):
            lib_file_name = '' + lib_folder_name + '/' + lib_file + '/' + lib_file + '.xml'
        else:
            lib_file_name = '' + lib_folder_name + '/' + lib_file + '/' + 'manifest.xml'
        soup = BeautifulSoup(open(lib_file_name, encoding='utf-8'), 'lxml-xml')
        soup = cleanComments(soup)
        if soup.find(recursive=False).name == 'Template':
            lib_mode = 1
        elif soup.find(recursive=False).name == 'ROOT':
            lib_mode = 0
        # print(lib_file, lib_mode)
    else:
        # V2
        lib_mode = 2
        plugin_file_name = plugin_src + '/' + 'manifest.xml'
        soup = BeautifulSoup(open(plugin_file_name, encoding='utf-8'), 'lxml-xml')
        soup = cleanComments(soup)

    return soup.prettify(), lib_mode


def getBsAttrs(soup, value):
    soup = BeautifulSoup(str(soup[0]), 'lxml-xml')
    for attr in soup.find_all(True, limit=1):
        if attr.get(value):
            result = attr['value']
        else:
            result = '0'
    return result


# 解析XML文件，重新整理属性，开始之前
def parseXML(parse_xml):
    global manifest_root, manifest_sw, manifest_sh, _dev_time

    # 读取文件内容
    with open(parse_xml, 'r') as file:
        content = file.read()
        print(content)
    content = content.replace('&gt;', '&amp;gt;')
    content = content.replace('&lt;', '&amp;lt;')
    # 将替换后的内容写回文件
    with open(parse_xml, 'w', encoding='utf-8') as file:
        file.write(content)

    _soup = BeautifulSoup(open(parse_xml, encoding='utf-8'), 'lxml-xml')

    # 输出根标签
    # for root in _soup.find_all(True, limit=1):
    #     manifest_root = str(root.name)
    #     manifest_sw = int(root.get('screenWidth'))
    #     manifest_sh = int(root.get('screenHeight', -1))
    root = _soup.find(recursive=False)
    manifest_root = root.name
    manifest_sw = root.get('screenWidth', 1080)
    manifest_sh = root.get('screenHeight', -1)

    # 注释清理
    _soup = cleanComments(_soup)

    # 删除原本的Key
    key_store = not RELEASE
    if key_store:
        keygen = _soup.find('Var', {'name': 'Key'})
        if keygen:
            keygen_string = keygen['expression']

            var_dict = eval(aes_decode(keygen_string))
            print(f"Deleted Origin Key ({len(var_dict)}, {len(keygen_string)}):\n {var_dict}")
            keygen.extract()

    # 删除 globalPersist 变量的 persist 属性
    for _p in _soup.find_all('Var', {'globalPersist': 'true'}):
        for _v in _soup.find_all('VariableCommand', {'name': _p.get('name')}):
            if _v.get('persist'):
                del _v['persist']

    _dev_time = getTimeSys()
    _soup_indent = str(_soup.prettify()).replace('\n', '').replace('$_devTime', str(_dev_time))
    _soup = BeautifulSoup(_soup_indent, 'lxml-xml')

    return _soup


# 保存XML文件，minidom格式化处理
def saveXML(soup, save_file):
    global var_split_ext
    global var_split_group
    global var_alias

    print('\t')
    print(f"LangsId: {langs_id}")
    print(f'Root: {manifest_root}')
    print(f'Width: {manifest_sw}')
    print(f'Height: {manifest_sh}')

    soup_dom_str = str(soup.prettify())
    soup_dom_str = soup_dom_str.replace(manifest_root, 'Lockscreen')
    soup_dom_str = soup_dom_str.replace('persist_const', var_persist_attr)

    soup = BeautifulSoup(soup_dom_str, features="lxml-xml")
    _soup = cleanComments(soup)

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

    var_procress_honor = 0 if str(_soup.Lockscreen.get('_processHonorVar')).upper() == "FALSE" or _soup.Lockscreen.get(
        '_processHonorVar') == "0" else 1
    print(f'Root[_processHonorVar]: {var_procress_honor}')

    if _soup.Lockscreen.get('_splitExt') is not None:
        del _soup.Lockscreen['_splitExt']
    if _soup.Lockscreen.get('_splitGroup') is not None:
        del _soup.Lockscreen['_splitGroup']
    if _soup.Lockscreen.get('_preload') is not None:
        del _soup.Lockscreen['_preload']
    if _soup.Lockscreen.get('_getSource') is not None:
        del _soup.Lockscreen['_getSource']

    if manifest_root == 'Lockscreen' or langs_id != 4 or manifest_root == 'Widget':

        # Parse Function Beta
        def parse_function_beta(fun_soup):
            for FunCom in fun_soup.find_all('FunCom'):
                FunName = FunCom.get('target')
                FunParams = FunCom.get('params', "{'': ''}")
                FunCondition = FunCom.get('condition')
                if FunName:
                    if FunParams:
                        FunParams = eval(FunParams)
                    # print(FunCom, FunParams, len(FunParams))
                    FoundFun = False
                    for FunTag in fun_soup.find_all('Fun', {'name': FunName}):
                        FunParamsCount = FunTag.get('count', '0')
                        if int(FunParamsCount) != len(FunParams) and int(FunParamsCount) != 0:
                            print('Check Params Count! \n')
                            sys.exit(1)
                        else:
                            for key, value in FunParams.items():
                                FunTag = str(FunTag).replace(f'{{{key}}}', value)
                                FunTag = BeautifulSoup(str(FunTag), 'lxml-xml')
                                if FunCondition:
                                    for tag in FunTag.find_all():
                                        if tag.name.endswith('Command'):
                                            tag_condition = tag.get('condition', '1')
                                            tag['condition'] = f'{tag_condition}*({FunCondition})'
                                            print(tag)
                            for F in range(len(FunTag.Fun.contents)):
                                FunContent = str(FunTag.Fun.contents[F])
                                FunContent = BeautifulSoup(f'{FunContent}', 'lxml-xml')
                                FunCom.insert_before(FunContent)
                            FunCom.extract()
                            FoundFun = True
                    if not FoundFun:
                        print("Check FunTag! \n")
                        sys.exit(1)
                else:
                    print("Check FunCom Tag! \n")
                    sys.exit(1)
            for FunTag in fun_soup.find_all('Fun'):
                FunTag.extract()
            return fun_soup

        _soup = parse_function_beta(_soup)

        # TextSize处理
        # text_size = []
        if not RELEASE:
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
        from tools.arrayc import c_array
        for code in _soup.find_all('C_Array'):
            # print(code)
            c_array_r = c_array(str(code))
            # print(c_array_r)
            code.insert_after(c_array_r)
            code.extract()

        # 历史遗漏：C_Array嵌套问题

        for image in _soup.find_all('Image'):
            pivotX = "$self.w/2-$self.x+#3D_centerX_2"
            pivotY = "$self.h/2-$self.y+#_py"
            rotation = "#_r*#3D_rotationX_2"

            image_x = image.get('x')
            image_y = image.get('y')
            image_w = image.get('w')
            image_h = image.get('h')
            image_rotation = image.get('rotation')
            image_px = image.get('pivotX')
            image_py = image.get('pivotY')
            if '$' in str(image_px):
                image['pivotX'] = image_px.replace('$self.w', image_w).replace('$self.x', image_x)
            if '$' in str(image_py):
                image['pivotY'] = image_py.replace('$self.h', image_h).replace('$self.y', image_y)
            if '$' in str(image_rotation):
                image['rotation'] = image_rotation.replace('$self.w', image_w).replace('$self.x', image_x).replace('$self.h', image_h).replace('$self.y', image_y)

        # 若 Image['rotation'] == '0' del Image['pivotX'], Image['pivotY'], Image['rotation'] // HONOR
        for image in _soup.find_all(['Image', 'Rectangle']):
            image_w = image.get('w')
            image_h = image.get('h')
            image_px = image.get('pivotX')
            image_py = image.get('pivotY')
            image_r = image.get('rotation')
            image_s = image.get('scale')
            image_v = image.get('visibility', '1')
            if image_r == '0' and not image_s:
                del image['rotation']
                if image_px == f"{image_w}/2" and image_py == f"{image_h}/2":
                    del image['pivotX'], image['pivotY']
            if image.get('act'):
                _action = image.get('act')
                _action_list_ = _action.split(',')
                if len(_action_list_) == 1:
                    _action_ = 'up'
                    _action_tag_id_ = str(_action_list_[0])
                elif len(_action_list_) == 2:
                    _action_ = str(_action_list_[0])
                    _action_tag_id_ = str(_action_list_[1])
                else:
                    _action_ = None
                    _action_tag_id_ = None
                # _action_ = str(_action.split(',')[0])
                # _action_tag_id_ = str(_action.split(',')[1])
                # print(_action_, _action_tag_id_)
                # time.sleep(10)

                _action_condition = '1'
                _action_visibility = '1'
                _action_content = ''
                for ac in _soup.find_all():
                    if ac.name == _action_tag_id_ \
                            or (ac.name == 'Compose' and ac.get('class') == _action_tag_id_) \
                            or (ac.name == 'Compose' and ac.get('act') == _action_tag_id_):
                        _action_condition = ac.get('condition', '1')
                        _action_visibility = ac.get('visibility', '1')
                        ac_contents = [item for item in ac.contents if item != '\n']
                        _action_content = str(ac_contents).replace('[', '').replace(']', '')
                        ac.extract()
                # _action_content = BeautifulSoup(_action_content, 'lxml-xml')

                # 创建 Button 标签
                _action_button = _soup.new_tag('Button')
                _action_triggers = _soup.new_tag('Triggers')
                _action_trigger = _soup.new_tag('Trigger')
                _action_trigger['action'] = _action_
                if _action_condition and _action_condition != '1':
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
                _action_button['visibility'] = f"({image_v})*({_action_visibility})"

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

    soup_dom_str = str(_soup.prettify()).replace('    ', '\t')
    with open(save_file, 'w', encoding='utf-8') as _f0:
        _f0.write(soup_dom_str)

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

    if var_str_num > 0:
        splitVar(success_xml, success_xml)
    if var_split_ext:
        splitExt(success_xml)
    if var_binders_num > 1:
        splitBinders(success_xml)
    if var_preload:
        preLoadVar(success_xml)
        preLoadExt(success_xml)
    if var_split_group:
        splitGroup(success_xml, manifest_root)
    intentMarket(success_xml, manifest_root)

    return 'TEST'


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
    global config_soup_str, var_config_soup_str, var_alias_dict

    var_alias_dict = {}
    _var_from_xml = []

    # var_alias = 1
    global _success_xml
    _success_xml = maml_main_xml.replace(maml_rule_file, 'manifest')
    _origin_xml = "source.xml"
    _anti_xml = "anti.xml"
    _anti_list_xml = "disable.xml"
    _source_xml = maml_main_xml.replace(maml_rule_file, 'source')

    # shutil.copy2(_success_xml, _origin_xml)

    # # 筛选name及target，并添加后缀（6位随机数）

    _var_alias_all = 1
    if _var_alias_all:
        refactor(_success_xml, 0, var_forbid_name, _success_xml)

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

        var_alias_dict = dev.Refactor.refactor.get_var_alias_dict(_anti_xml)
        # print(var_alias_dict)

        for after, initial in var_alias_dict.items():

            # 替换【config.xml】内的变量
            if os.path.exists(config_xml):
                config_soup_str = config_soup_str.replace('id="' + initial + '"', 'id="' + after + '"')

            # 替换【var_config.xml】内的变量
            if os.path.exists(var_config_xml):
                var_config_soup_str = var_config_soup_str.replace('name="' + initial + '"',
                                                                  'name="' + after + '"').replace(
                    'repeatVar="' + initial + '"', 'repeatVar="' + after + '"')

        # 保存【config.xml】
        if os.path.exists(config_xml):
            with open(config_xml, 'w', encoding='utf-8') as _f0:
                _f0.write(config_soup_str.replace('\n', ''))

        # 保存【var_config.xml】
        if os.path.exists(var_config_xml):
            with open(var_config_xml, 'w', encoding='utf-8') as _f0:
                _f0.write(var_config_soup_str.replace('\n', ''))

        # 删除无用的变量动画
        _soup_final = BeautifulSoup(open(_success_xml, 'rb'), features="lxml-xml")
        import copy
        _soup_final2 = copy.copy(_soup_final)
        for var_tag in _soup_final2.find_all('Var'):
            if var_tag.VariableAnimation:
                var_tag.decompose()
        _soup_temp = str(_soup_final2)
        # print(f'删除变量动画: {_soup_temp})

        # 删除无用的变量 BETA ==> VariableCommand // 2024.07.10
        for var_tag in _soup_final.find_all('VariableCommand'):
            var_search = var_tag.get('name')

            # 两种情况下不删除: 1:[#|@]{varName} 2:声明变量Var
            if f'#{var_search}' in str(_soup_final) or f'@{var_search}' in str(_soup_final)\
                    or f'name="{var_search}"' in str(_soup_final):
                pass
            else:
                # print(var_tag)
                var_tag.extract()

        _vars = []
        # 遍历Var标签
        for var_tag in _soup_final.find_all('Var'):
            if var_tag.VariableAnimation:
                var_name = '#' + str(var_tag.get('name'))
                var_name_e = str(var_tag.get('name'))
                # 排除默认动画变量 looping
                if (var_tag.get('name') and var_tag.get('_glb') is None
                        and str(var_alias_dict[var_name_e]) not in ['looping']):
                    var_content = str(var_tag)

                    if var_name in var_content and var_name not in _soup_temp:
                        _vars.append(var_name_e)
                    elif var_name in var_content and var_name in _soup_temp:
                        origin_var_e = var_alias_dict[var_name_e]
                        print(f"Exist: {{'{origin_var_e}': '{var_name_e}'}}")
                    elif var_name not in var_content and var_name not in _soup_temp:
                        _vars.append(var_name_e)

        # print(var_alias_dict)
        print('Decompose:')
        for _i in range(len(_vars)):
            origin_var = var_alias_dict[_vars[_i]]
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
            if _tags.name == 'StereoView':
                stereo_w = _tags.get('w', '1')
                stereo_h = _tags.get('h', '1')
                _image_dict = {
                    'x': '0',
                    'y': '0',
                    'w': stereo_w,
                    'h': stereo_h,
                    'src': 'bg.png',
                    'alpha': '1'
                }
                for _group in _tags.find_all('StereoGroup'):
                    _image_slot = _soup_final.new_tag('Image', attrs=_image_dict)
                    _group.insert(0, _image_slot)

        # 删除空闲 threshold
        for var in _soup_final.find_all('Var'):
            if var.parent.name == 'StereoGroup':
                var.extract()
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
            if _del_tag.get('disabled') is not None and _del_tag.get('disabled') != '0':
                # print(_del_tag)
                _del_tag.decompose()
            else:
                _button_x = _del_tag.get('x')
                _button_y = _del_tag.get('y')
                _button_w = _del_tag.get('w')
                _button_h = _del_tag.get('h')

                _button_align = _del_tag.get('align')
                _button_alignV = _del_tag.get('alignV')

                _button_x_left = _button_x
                _button_x_center = evalNum(f'({_button_x})-int(({_button_w})/2)')
                _button_x_right = evalNum(f'({_button_x})-int(({_button_w}))')

                _button_y_top = _button_y
                _button_y_center = evalNum(f'({_button_y})-int(({_button_h})/2)')
                _button_y_bottom = evalNum(f'({_button_y})-int(({_button_h}))')

                if _button_align:
                    exec(f"_del_tag['x'] = _button_x_{_button_align}")
                    del _del_tag['align']

                if _button_alignV:
                    exec(f"_del_tag['y'] = _button_y_{_button_alignV}")
                    del _del_tag['alignV']

        # 若变量动画 改变帧率控制器 自动获取最大时间 FOR 小米小部件
        if _soup_final.FramerateController and manifest_root == 'Widget':
            frame_control_time = [0, 100, 101]
            frame_time_collect = []
            for frame_control in _soup_final.find_all():
                if frame_control.get('_e') != '1' and (
                        frame_control.name == 'Item' or frame_control.name == 'AniFrame') and (
                        (frame_control.get('time') and frame_control.get('time').isdigit()) or (
                        frame_control.get('dtime') and frame_control.get('dtime').isdigit())):
                    if frame_control.get('time'):
                        frame_time_collect.append(frame_control.get('time'))
                        print(frame_control['time'])
                    if frame_control.get('dtime'):
                        frame_time_collect.append(str(int(frame_control.get('dtime')) * 2))
                    print(frame_time_collect)
                    frame_time_collect.sort(key=lambda x: (int(x), x), reverse=True)

            for frame_control in _soup_final.find_all():
                if frame_control.get('_e') != '1' and (
                        frame_control.name == 'Item' or frame_control.name == 'AniFrame') and (
                        (frame_control.get('time') and frame_control.get('time').isdigit()) or (
                        frame_control.get('dtime') and frame_control.get('dtime').isdigit())):
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

        # 带 condition 属性的 SoundCommand 标签单独处理（新增 _condition 属性屏蔽处理）
        print('SoundCommand: ')
        _sound_collect = []
        for sound in _soup_final.find_all('SoundCommand'):
            if sound.get('condition') is not None and sound.get('_condition') is None:
                print(f"\t{sound}")

                time_sys = str(time.time())
                sound_thrs_uuid = sound.encode('UTF-8')
                sound_thrs_uuid2 = hex(zlib.crc32(time_sys.encode('UTF-8')))[2:].capitalize()
                sound_thrs_name = hex(zlib.crc32(sound_thrs_uuid))[2:].capitalize() + sound_thrs_uuid2
                # print(sound_thrs_name)

                new_sound_var = soup.new_tag('VariableCommand')
                new_sound_var['name'] = sound_thrs_name
                new_sound_var['expression'] = f'#{sound_thrs_name}+1'
                new_sound_var['type'] = 'number'
                new_sound_var['condition'] = sound['condition']
                sound.insert_after(new_sound_var)

                new_sound_thrs = soup.new_tag('Var')
                new_sound_thrs['name'] = f'__{sound_thrs_name}'
                new_sound_thrs['expression'] = f'#{sound_thrs_name}'
                new_sound_thrs['threshold'] = '1'
                new_sound_thrs['type'] = 'number'
                new_sound_thrs_t = soup.new_tag('Trigger')
                new_sound_thrs_c = BeautifulSoup(str(sound).replace('condition', 'alias'), 'lxml-xml')
                new_sound_thrs_t.append(new_sound_thrs_c)
                # print(new_sound_thrs_t)
                new_sound_thrs.append(new_sound_thrs_t)
                # print(new_sound_thrs)
                _sound_collect.append(new_sound_thrs)
                # print(sound.parent)
                sound.decompose()
                # print(str(_soup_final))
        # print(_sound_collect)
        for _s in range(len(_sound_collect)):
            _soup_final.Lockscreen.append(_sound_collect[_s])
        # print(_soup_final)
        # time.sleep(10000)
        print('\t')

        # 优化 Rectangle['cornerRadius']
        for rect in _soup_final.find_all('Rectangle'):
            cornrer = rect.get('cornerRadius')
            if cornrer and ',' not in str(cornrer):
                rect['cornerRadius'] = f'{cornrer},{cornrer}'

        # eval {eval_content} eg: "{0+1}" => "1"
        # Beta Test
        # print('Eval Debug:')
        # from tools.arrayc import eval_soup, eval_safe, eval_decimal
        #
        # def do_eval_action(_soup_final):
        #     _soup_ = eval_soup(_soup_final, 0)
        #     _soup_final = _soup_[0]
        #     var_dict = _soup_[1]
        #
        #     # if any(char in var_dict for char in ['{', '}', '#']):
        #     #     do_eval_action(_soup_final)
        #
        #     # 根据键的长度对字典进行排序
        #     print('Eval Var: ')
        #     sorted_dict = dict(sorted(var_dict.items(), key=lambda x: len(var_alias_dict[str(x[0])[1:]])))
        #
        #     # 打印排序后的值
        #     sorted_content = '\t '
        #     for key, value in sorted_dict.items():
        #         sorted_content = f'{sorted_content}{key}: ({var_alias_dict[str(key)[1:]]}) => {str(value)}\n\t '
        #     print(sorted_content)
        #
        #     return _soup_final
        #
        # _soup_final = do_eval_action(_soup_final)

        # 若预览器需要改变量的值，不需要开启 eval_all_mode
        # eval_all_mode = 0
        # if eval_all_mode:
        #     for key, value in var_dict.items():
        #         if str(key)[1:] not in var_forbid_name:
        #             print('\t', str(var_alias_dict[str(key[1:])]), value)
        #             _soup_final = BeautifulSoup(str(_soup_final).replace(key, value), 'lxml-xml')

        # 处理按钮负值
        # if eval_all_mode:
        #     for eval_tag in _soup_final.find_all():
        #         for attr, value in eval_tag.attrs.items():
        #             if str(value).startswith('-'):
        #                 value = '0' + str(value)
        #                 eval_tag[attr] = value
        #                 print(value)
        #             else:
        #                 eval_tag[attr] = eval_decimal(value)

        print('\t')

        # eval 之后删除无用变量数组 Var[]
        # for var in _soup_final.find_all('Var'):
        #     var_type = var.get('type')
        #     if str(var_type).startswith('number[]') and f'#{var_type}' not in str(_soup_final) or \
        #             str(var_type).startswith('string[]') and f'@{var_type}' not in str(_soup_final):
        #         var.decompose()
        #     else:
        #         pass

        # 保存前的最后一步: 定义一个函数用于将中文和特殊字符转换为 Unicode 字符串
        unicode_mode = 0
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
                        if '://' in str(string_value) and all(
                                forbidden_char not in str(string_value) for forbidden_char in "#@"):
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
                if image.get('src') and 'srcid' in image.attrs and image.get(
                        '_src_exp_mode') != '0' and '.9' not in image.get('src'):
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
                    # image['srcExp'] = "'" + image_filename + "_'+" + image_srcid_a + image_srcid + image_srcid_b +
                    # "+'." + image_suffix + "'"
                    image[
                        'srcExp'] = f"'{image_filename}_'+{image_srcid_a}{image_srcid}{image_srcid_b}+'.{image_suffix}'"

                    print(f"\t{image['srcExp']}")
                    del image['src']
                    del image['srcid']
            print('\t')

        # 存储Key
        key_store = not RELEASE
        if manifest_root == 'Lockscreen' and key_store:
            # 找到了满足条件的标签
            # 执行你的代码
            key_var = _soup_final.new_tag('Var')
            key_var['name'] = 'Key'
            key_var['expression'] = f"'{aes_encode(str(var_alias_dict).strip())}'"
            # key_var['type'] = 'byteArray'
            key_var['type'] = 'string'
            try:
                _soup_final.Lockscreen.Var.insert_before(key_var)
            except Exception as _key_e:
                print('Var is not exists!', _key_e)

        soup_dom_str = str(_soup_final.prettify()) \
            .replace('    ', '\t').replace('&amp;#', '&#') \
            .replace('__widget_auto_size__', maml_folder_name.replace('widget_', ''))

        # 检测/移除空属性
        for element in _soup_final.find_all():
            if '[]' not in str(element):
                # 遍历元素的所有属性
                for attr_name, attr_value in element.attrs.items():
                    if attr_value == '' or str(attr_value).strip() == '':
                        print(f'⚠️Warning: {element}')
        # time.sleep(1)

    with open(_success_xml, 'w', encoding='utf-8') as _f0:
        if var_alias:
            _f0.write(soup_dom_str.replace('\n', '').replace('&amp;#', '&#'))
        else:
            _f0.write(soup_dom_str.replace('&amp;#', '&#'))

    order_xml_mode = 1
    if order_xml_mode:
        import tools.order
        tools.order.orderXML(_success_xml, None, 0)
    if var_get_source:
        if 'Key' in soup_dom_str:
            import tools.anti_new
            tools.anti_new.convert_to_source(_success_xml, _source_xml, 0)
        else:
            import tools.anti
            tools.anti.convert_to_source(_anti_xml, _success_xml, _source_xml, 1, 0)

    # End

    return


# 主程序
lib = dirLib(lib_folder_name)
shutil.copy(maml_main_xml, parse_xml)
soup = parseXML(parse_xml)
_lib_soup_json_ = {}
_lib_soup_json_r_ = {}
_lib_soup_id_ = {}

print('Disabled:')
# Main / Start / 开始
global _id_local_
for tag in soup.find_all(True):

    # 检测【disabled】属性是否存在，若存在则删除标签，并重新写入soup
    if tag.get('disabled') is None:
        tag.disabled = 0
    elif tag.get('disabled') == '0':
        tag.disabled = 0
    else:
        tag.disabled = int(tag.get('disabled'))

    if tag.disabled or tag.name == 'i_Hidden':
        # print(f'\t{tag.name}.extract()')
        tag.extract()
        _id_local_ = ''

    else:

        # 匹配库文件标签
        for i in range(len(lib)):
            if tag.name == lib[i] and tag.get('card') not in ['Almanac', 'Constellations', 'BigEvent']:
                if 1:
                    _lib_callback_ = getLibFile(tag.name)[0]
                    _lib_soup_ = BeautifulSoup(str(_lib_callback_), 'lxml-xml')
                    _lib_mode_ = getLibFile(tag.name)[1]
                    if tag.get('_id') is None:
                        _lib_id_ = ''
                    else:
                        _lib_id_ = '_' + tag.get('_id')

                    # [ROOT] MODE
                    if _lib_mode_ == 0:
                        _value_holder_ = _lib_soup_.find_all('ValueHolder')
                        for _value_ in range(len(_value_holder_)):
                            _holder_name_ = _value_holder_[_value_].get('name')
                            _holder_value_def_ = _value_holder_[_value_].get('default')
                            _holder_value_ = tag.find_all(name='ValueHolder', attrs={'name': _holder_name_})
                            if _holder_value_:
                                _holder_value_ = getBsAttrs(_holder_value_, 'value')
                            else:
                                # ROOT.ValueHolder 默认值分配
                                _holder_value_ = _holder_value_def_
                            _lib_soup_ = str(_lib_soup_).replace(_holder_name_, _holder_value_)
                        _lib_soup_ = BeautifulSoup(str(_lib_soup_), 'lxml-xml')
                        for _value_tag_ in _lib_soup_.find_all('ValueHolder'):
                            _value_tag_.extract()

                        for _place_holder_ in _lib_soup_.find_all('PlaceHolder'):
                            if _place_holder_.get('name'):
                                _place_name_ = _place_holder_.get('name')
                                for _place_in_ in soup.find_all(_place_name_):
                                    _place_in_null_ = len(_place_in_.contents) == 1 and str(_place_in_.contents[0]).strip() == ''
                                    if not _place_in_null_:
                                        for _p_in_ in range(len(_place_in_.contents) - 1, -1, -1):
                                            _p_insert_contents_ = _place_in_.contents[_p_in_]
                                            _p_insert_ = BeautifulSoup(str(_p_insert_contents_), 'lxml-xml')
                                            # print(len(_p_insert_))
                                            if len(_p_insert_) and _place_holder_.parent:
                                                _place_holder_.insert_after(_p_insert_)
                                    _place_holder_.extract()

                        with open(process_xml, 'w', encoding='utf-8') as f:
                            f.write(str(_lib_soup_))
                        refactor(process_xml, 2, var_forbid_name, _lib_id_)
                        _lib_soup_ = BeautifulSoup(open(process_xml, encoding='utf-8'), 'lxml-xml')

                        # print(process_xml, _lib_soup_)
                        # print(_lib_soup_.Template)

                        if 1:
                            for _in_ in range(len(_lib_soup_.ROOT.contents) - 1, -1, -1):
                                _insert_contents_ = _lib_soup_.ROOT.contents[_in_]
                                # print(_insert_contents_)
                                _insert_ = BeautifulSoup(str(_insert_contents_), 'lxml-xml')
                                tag.insert_after(_insert_)
                            tag.extract()

                    # [Template] MODE
                    elif _lib_mode_ == 1:
                        if _lib_soup_.Props:
                            _props_ = _lib_soup_.find_all('Props')[0].find_all('item')
                            _props_item_ = {}
                            for _item_ in _props_:
                                # print(_item_['name'], _item_['default'])
                                for key, value in _item_.attrs.items():
                                    _props_item_[_item_['name']] = _item_['default']
                                _props_item_ = dict(sorted(_props_item_.items(), key=lambda item: len(item[0]), reverse=True))
                            # print(_props_item_)

                            for attr, value in tag.attrs.items():
                                for item_key, item_value in _props_item_.items():
                                    if str(item_key) == str(attr):
                                        _props_item_[item_key] = str(value)
                            # print(_props_item_)

                            for key, value in _props_item_.items():
                                _lib_soup_ = str(_lib_soup_).replace(f'${str(key)}', str(value))
                            _lib_soup_ = BeautifulSoup(_lib_soup_, 'lxml-xml')
                            for _props_tag_ in _lib_soup_.find_all('Props'):
                                _props_tag_.extract()

                        with open(process_xml, 'w', encoding='utf-8') as f:
                            f.write(str(_lib_soup_))
                        refactor(process_xml, 2, var_forbid_name, _lib_id_)
                        _lib_soup_ = BeautifulSoup(open(process_xml, encoding='utf-8'), 'lxml-xml')

                        for _pro_in_ in range(len(_lib_soup_.Template.contents) - 1, -1, -1):
                            _pro_insert_contents_ = _lib_soup_.Template.contents[_pro_in_]
                            # print(_pro_insert_contents_)
                            _pro_insert_ = BeautifulSoup(str(_pro_insert_contents_), 'lxml-xml')
                            tag.insert_after(_pro_insert_)
                        tag.extract()

                    else:
                        print('"_lib_mode_" is greater than 1! ')

        if tag.get('src'):
            _state_name_ = tag.get('src').split('/')[-1] + '.'
            _state_name_ = 'state.'

        if tag.name == 'Plugin':

            # 该函数不可移动位置

            def _module_add_(module_tag='', main_tag='', module_soup='', tag=''):
                if module_tag and main_tag and module_soup:
                    while module_soup.find_all(module_tag):
                        for slot in tag.find_all(main_tag, limit=1):
                            for slots in module_soup.find_all(module_tag, limit=1):
                                _slot_ = list(slot.contents)
                                if module_tag == 'Emits':
                                    _button_ = _lib_soup_.new_tag('Button', attrs=slots.attrs)
                                    for _s_ in range(len(_slot_) - 1, -1, -1):
                                        _button_.append(BeautifulSoup(str(_slot_[_s_]), 'lxml-xml'))
                                    # _button_['x'] = _props_item_['x']
                                    # _button_['y'] = _props_item_['y']
                                    # _button_['w'] = _props_item_['w']
                                    # _button_['h'] = _props_item_['h']
                                    # print(_button_)
                                    # sys.exit(8)
                                    slots.insert_after(_button_)
                                elif module_tag == 'Slots':
                                    _group_ = _lib_soup_.new_tag('Group', attrs=slots.attrs)
                                    print(_group_)
                                    for _s_ in range(len(_slot_) - 1, -1, -1):
                                        _group_.append(BeautifulSoup(str(_slot_[_s_]), 'lxml-xml'))
                                    slots.insert_after(_group_)
                                else:
                                    for _s_ in range(len(_slot_) - 1, -1, -1):
                                        slots.insert_after(BeautifulSoup(str(_slot_[_s_]), 'lxml-xml'))
                                slots.extract()
                    return module_soup
                else:
                    print('请检查 Plugin 标签！')
                    sys.exit(0)

            _lib_callback_ = getLibFile(tag.name, 2, tag.get('src'))[0]
            _lib_soup_ = BeautifulSoup(str(_lib_callback_), 'lxml-xml')
            _lib_mode_ = getLibFile(tag.name, 2, tag.get('src'))[1]
            if tag.get('_id') is None:
                _lib_id_ = '_' + hex(int(time.time() * 1000))[-7:-1]
                library_mode = 2
            else:
                _lib_id_ = '_' + tag.get('_id')
                library_mode = 2

            # [Template] MODE [version=2]
            if _lib_mode_ == 2:
                if _lib_soup_.Props:
                    _props_ = _lib_soup_.find_all('Props')[0].find_all('item')
                    _props_item_ = {}
                    _props_item_type_ = {}
                    for _item_ in _props_:
                        # print(_item_['name'], _item_['default'])
                        for key, value in _item_.attrs.items():
                            _props_item_[_item_['name']] = _item_['default']
                            _props_item_type_[_item_['name']] = _item_['type']
                        _props_item_ = dict(sorted(_props_item_.items(), key=lambda item: len(item[0]), reverse=True))
                        _props_item_type_ = dict(sorted(_props_item_type_.items(), key=lambda item: len(item[0]), reverse=True))
                    # print(_props_item_)
                    # print(_props_item_type_)

                    for attr, value in tag.attrs.items():
                        for item_key, item_value in _props_item_.items():
                            if str(item_key) == str(attr):
                                _props_item_[item_key] = str(value)

                    for key, value in _props_item_.items():
                        if _props_item_type_[key] not in ['select', 'bool']:
                            _lib_soup_ = str(_lib_soup_).replace(f'${str(key)}', str(value))
                        elif _props_item_type_[key] == 'select':
                            _lib_soup_ = BeautifulSoup(str(_lib_soup_), 'lxml-xml')
                            for _select_ in _lib_soup_.find_all('Select', attrs={'index': f'${str(key)}'}):
                                # print(_select_, value)
                                _select_tag_ = _select_.find_all('Item')[int(value)]
                                # print(_select_tag_)
                                for _slt_ in list(_select_tag_.contents):
                                    _select_.parent.append(_slt_)
                                _select_.extract()
                                # print(_lib_soup_)
                            _lib_soup_ = BeautifulSoup(str(_lib_soup_), 'lxml-xml')
                        elif _props_item_type_[key] == 'bool':
                            _lib_soup_ = str(_lib_soup_).replace(f'${str(key)}', str(value))
                            _lib_soup_ = BeautifulSoup(str(_lib_soup_), 'lxml-xml')
                            for _inset_ in _lib_soup_.find_all(True):
                                _bool_ = str(_inset_.get('inset', True)).upper() == 'TRUE'
                                if _bool_ is False:
                                    _inset_.extract()
                                else:
                                    del _inset_['inset']
                            _lib_soup_ = BeautifulSoup(str(_lib_soup_), 'lxml-xml')

                            # print(_props_item_[key])
                    _lib_soup_ = BeautifulSoup(_lib_soup_, 'lxml-xml')

                    for _props_tag_ in _lib_soup_.find_all('Props'):
                        _props_tag_.extract()

                    # print(_lib_soup_)

                if tag.Slot:
                    _lib_soup_ = _module_add_('Slots', 'Slot', _lib_soup_, tag)
                if tag.Animation:
                    _lib_soup_ = _module_add_('Animations', 'Animation', _lib_soup_, tag)
                if tag.Emit:
                    _lib_soup_ = _module_add_('Emits', 'Emit', _lib_soup_, tag)

                # 注意:动画仅支持元素动画的添加

                # for _item_ in _lib_soup_.find_all('Item', attrs=None):
                #     _item_.extract()

                with open(process_xml, 'w', encoding='utf-8') as f:
                    f.write(str(_lib_soup_))
                _lib_soup_json_[tag.get('name')] = _lib_soup_

                # refactor(process_xml, library_mode, var_forbid_name, _lib_id_)
                _lib_soup_id_[tag.get('name')] = '_' + str(refactor(process_xml, library_mode, var_forbid_name, _lib_id_))
                _id_local_ = _lib_id_[1:]

                _lib_soup_ = BeautifulSoup(open(process_xml, encoding='utf-8'), 'lxml-xml')

                # if _id_local_:
                #     _id_tag_ = _lib_soup_.new_tag('Var', attrs={'name': f"$_id_{_id_local_}$", 'expression': f"'{_id_local_}'", 'type': 'string'})
                #     _lib_soup_.Template.append(_id_tag_)

                _pro_group_ = _lib_soup_.new_tag('Group', attrs={'name': tag.get('name')})
                for _pro_in_ in range(len(_lib_soup_.Template.contents)):
                    _pro_insert_contents_ = _lib_soup_.Template.contents[_pro_in_]
                    # print(_pro_insert_contents_)
                    _pro_insert_ = BeautifulSoup(str(_pro_insert_contents_), 'lxml-xml')
                    _pro_group_.append(_pro_insert_)
                tag.insert_after(_pro_group_)
                _lib_soup_json_r_[tag.get('name')] = _pro_group_

                tag.extract()

        if tag.name == 'Store':
            _lib_callback_ = getLibFile(tag.name, 2, tag.get('src'))[0]
            _lib_soup_ = BeautifulSoup(str(_lib_callback_), 'lxml-xml')
            _lib_mode_ = getLibFile(tag.name, 2, tag.get('src'))[1]

            # [Template] MODE [version=2]
            if _lib_mode_ == 2:
                for var in _lib_soup_.find_all('Var'):
                    var['name'] = f"{_state_name_}{var.get('name')}"
                    tag.insert_after(var)
                tag.extract()

        if tag.name == 'StoreCommit':
            # [Template] MODE [version=2]
            tag.name = 'VariableCommand'
            tag['name'] = _state_name_ + tag.get('name')

        def _plugin_get(plugin, foo, src):
            plugin = plugin.replace('$', '')
            if foo[0] == '#':
                foo_type = 'number'
            if foo[0] == '@':
                foo_type = 'string'
            foo = foo[1:]
            soup = BeautifulSoup(str(src), 'lxml-xml')
            bar = ''
            for var in soup.Template.find_all('Var', attrs={'name': foo}):
                if foo_type == 'string' and var.get('type') == 'string':
                    bar1 = var.get('expression')
                    bar = bar1
                if foo_type == 'number' and var.get('type') != 'string':
                    bar2 = var.get('expression')
                    bar = bar2
            return str(bar)

        for _attr, _value in tag.attrs.items():
            pattern = r'get\(\$([^,]+),([^,]+)\)'
            if re.search(pattern, _value):
                result = re.search(pattern, _value)
                result = result.group()
                rr_a = result.split('get(')[1]
                rr_b = rr_a.split(')')[0]
                rr_0 = rr_b.split(',')[0].replace('$', '')
                rr_1 = rr_b.split(',')[1]
                # exec(f'_plugin_{result.group()}')
                print('\t', str(f'[0xff{_id_local_}]'), rr_1, _id_local_)
                if rr_1 != '@_id':
                    replacement = _plugin_get(rr_0, rr_1, _lib_soup_json_[rr_0])
                else:
                    replacement = _id_local_
                print('\t', str(f'[0xff{_id_local_}]'), _value, ':', str(result), '==>', str(replacement))
                tag[_attr] = _value.replace(str(result), str(replacement))

            if _attr == 'bind':
                _bind_ = xml_var_alias(str(tag), str(tag), 2, var_forbid_name, _lib_soup_id_[_value])
                _bind_ = BeautifulSoup(_bind_, 'lxml-xml')
                for _b_ in _bind_.find_all(True):
                    if _b_.get('bind'):
                        del _b_['bind']
                tag.insert_after(_bind_)
                tag.extract()

# PluginCommands 替换法（需优化）

_plugin_content = {}
for tag in soup.find_all('PluginCommand'):
    _target = tag.get('target')
    _command = tag.get('command')
    _plg_tgr_contents = ''

    for _plg_grp in soup.find_all('Group'):
        if _plg_grp.get('name') == str(_target):
            for _plg_cmd in _plg_grp.find_all('PluginCommands'):
                for _plg_tgr in _plg_cmd.find_all('Trigger'):
                    if _plg_tgr.get('action') == str(_command):
                        for _ct in _plg_tgr.contents:
                            _plg_tgr_contents += str(_ct)
                        _plugin_content[(_target, _command, '_tag')] = (_plg_tgr_contents, str(tag))
                        # print('contents', _plg_tgr.contents)
# print(_plugin_content)

for tag in soup.find_all(True):
    if tag.name in ['PluginCommands', 'NameHolder']:
        tag.extract()

# 二维字典替换
for _k, _v in _plugin_content.items():
    soup = str(soup).replace(str(_v[1]), str(_v[0]))
    soup = BeautifulSoup(str(soup), 'lxml-xml')
    # print(soup)

for tag in soup.find_all('i_Hidden'):
    tag.decompose()

# 重新解析XML
dev_time = _dev_time
saveXML(soup, success_xml)

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

print(_success_xml)
print('>>>>>>')
with open(_success_xml, "rb") as file:
    result_xml_string = file.read()
    print(result_xml_string)
print('<<<<<<')


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
    return size_in_kb


def calculateMemory(folder_path=None):
    from PIL import Image

    if folder_path is None:
        folder_path = pyperclip.paste()

    folder_path_abs = folder_path.replace(maml_rule_file, '')
    folder_path = os.path.dirname(folder_path)

    total_memory = 0
    image_compress_ratio = 720 / 1080
    # image_compress_ratio = 1 / 960 * 720
    image_compress_mode = 0

    print(f'CompressMode: {image_compress_mode}')
    for _root, _, _files in os.walk(folder_path):
        if len(_files) <= 1000:
            for filename in _files:
                _file_path = os.path.join(_root, filename)
                _file_path_abs = _file_path.replace(folder_path_abs, '')

                if filename.startswith("._") or filename == ".DS_Store":
                    try:
                        os.remove(_file_path)
                        print(f'Remove: {filename}')
                    except Exception as _file_e:
                        pass
                        print(f"Exception: {_file_e}")

                if any(_file_path.endswith(ext) for ext in ['.xml', '.mp3', '.mp4', '.jpg']) or \
                        _file_path_abs.startswith('gitignore'):
                    continue  # 检查文件扩展名是否为.xml .mp3 .mp4 跳过
                try:
                    image = Image.open(_file_path)
                    width, height = image.size
                    memory_mb = width * height * 4 / (1024 * 1024)
                    # print(_file_path)

                    if not any(os.path.basename(_file_path) == ext for ext in ['bg.png', 'statusbar.png']):
                        if memory_mb >= 1.28:
                            # if memory_mb >= 3 and width > 720:
                            print(
                                f"Oversize: {width} x {height}, {_file_path_abs}, {memory_mb} MB")
                            if image_compress_mode:
                                # (_file_path_abs.startswith('assets') or _file_path_abs.startswith(
                                #     'bz')) and
                                new_width = int(width * image_compress_ratio)
                                new_height = int(height * image_compress_ratio)
                                resized_image = image.resize((new_width, new_height))
                                resized_image.save(_file_path)
                                new_memory_mb = new_width * new_height * 4 / (1024 * 1024)
                                print(f"Compressed: {new_width} x {new_height}, {_file_path_abs}, {new_memory_mb} MB")
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
    strict_mode = 1
    total_memory_unit = 1 if strict_mode else 0.88230
    total_memory_heytap = 2 * total_memory / (1024 * 1024)
    total_memory_harmony = (6 + 128 + total_memory_heytap)
    total_memory_origin = total_memory_unit * (total_memory_harmony + 300 * 0)
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
        os.rename(f"{os.path.join(os.path.dirname(_input_folder), base_folder_name)}.zip",
                  os.path.join(os.path.dirname(_input_folder), output_file_name))

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

if 'PYCHARM_HOSTED' in os.environ and maml_main_xml != local_xml and (
        maml_folder_name == 'advance' or maml_folder_name.startswith('widget')):
    calculateMemory()
    apply_test = 0
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
log_message = (f"Script Run Time: {run_time} seconds, <CompressRate value=\"{compress_rate}\" count=\"{count}\" "
               f"dev_time=\"{dev_time}\" />")
logging.info(log_message)

# 连接到数据库
conn = sqlite3.connect(os.path.join(database_path, "counter.db"))
conn.execute(
    "INSERT INTO counter (count, source, compress_rate, run_time, dev_time, anti_json) VALUES (?, ?, ?, ?, ?, ?)",
    (count, maml_main_xml, compress_rate, run_time, dev_time, str(var_alias_dict)))
conn.commit()
# 关闭数据库连接
conn.close()
sys.exit(0)
