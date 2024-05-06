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

# 03.30 需要修复使用Slot时，只能获取一行代码（目前的解决方案是用 <PlaceHolder name="Slot" /> 解决
# 03.30 加入TextSize特殊用法
# 05.08 转移到Mac本地，去除source.xml及maml.xml，直接从剪贴板读取maml.xml，并将文件生成其对应目录下；修改dll为本地路径（由于Mac没有Temp）
# 待同步至Windows
# 05.11 新增WidgetSu小部件代码模版
# 05.11 issue: PlaceHolder多行传值 / Slot传单值 PlaceHolder在每个lib只能有一个
# 05.15 issue important: .replace('#' + str(var_from_target[i]) + ', ' 逗号前去除空格 + '@'
# 05.16 修改intent库：浏览器, 计算器, 日历, 时钟
# 05.17 新增var_from_target: 收录countName
# 05.19 新增全局变量night_mode（未同步至CivetCode）
# 06.16 修改WeekCalendar库：新增系统字体写法（旧版本可能导致报错）
# 06.17 新增maml.xml根标签【_splitExt="0"】【_splitGroup="0"】属性，当为"0"或"false"时不进行对应操作
# 		若不存在属性则默认开启（针对小米主题Rocks）
# 06.19 新增移除所有alias属性（PSD切图时产生的文件注释）
# 06.25 issue important：解决Calendar标签为【card="Almanac"】时，取消模块替换
# 06.27 issue important：在编写带有【market】属性的Intent时，需注意Props属性读取先后顺序（如美团、饿了么）
# 07.08 新增标签顺序整理(preLoadVar, preLoadExt)：Lockscreen > ExternalCommands > VariableBinders > VariableAnimation >
# 		Var.threshold > Var > Weather > Calendar > Healthy > VarArray > ... > Group.Button
# 07.14 新增模块属性【disabled】，该属性存在时，对应模块不进行编译
#       优化数据库结构，清空使用次数及logging文件，已存放于su文件夹（2900 count）

import logging
import os
import random
import re
import shutil
import sqlite3
import time
import xml.dom.minidom
import zlib

import pyperclip
import requests
from bs4 import BeautifulSoup, Comment
from lxml import etree as lxml

from splitTools import splitVar, splitExt, splitBinders, splitGroup, preLoadVar, preLoadExt

maml_rule_file = "maml.xml"
maml_main_xml = pyperclip.paste()
maml_file_name = os.path.basename(maml_main_xml)

# 判断 maml_file_name 是否以 maml_rule_file 结尾
if not maml_file_name.endswith(maml_rule_file):
    print(f"Error: File must be '{maml_rule_file}'")
    exit(1)

print('\t')
print(f'Source: {maml_main_xml}')
# maml_main_xml = '/Users/wangshilong/Desktop/导出/待办/麦禾-木兰/19.浪漫米奇米妮锁屏切图/国内版/OPPO/lockscreen/advance/maml.xml'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='main.log')

start_time = time.time()  # 记录开始时间

orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


BeautifulSoup.prettify = prettify


# 连接到数据库
conn = sqlite3.connect('counter.db')

# 创建表格（如果不存在）
conn.execute('''CREATE TABLE IF NOT EXISTS counter
             (id INTEGER PRIMARY KEY,
             count INTEGER,
             source TEXT,
             compress_rate TEXT,
             run_time TEXT,
             dev_time TEXT);''')

# 读取计数器的值
cursor = conn.execute("SELECT count FROM counter WHERE id = 1")
row = cursor.fetchone()
if row is None:
    count = 0
else:
    count = row[0]

# 更新计数器并写入新的数据行
count += 1

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
                   'flashlight', 'flashlightValue', 'fod_enable', 'fod_height', 'fod_state_msg', 'fod_width', 'fod_x',
                   'fod_y', 'frame_rate', 'hasSteps', 'hasWeather', 'hassteps', 'health1', 'heart_rate_value', 'hour',
                   'hour12', 'hour24', 'isPreviewMode', 'isMatePad_H_2560', 'isMatePad_V_1600', 'isSupportMicro',
                   'is_music_playing', 'is_work_day', 'ishour12', 'lunarDay', 'lunarMonth', 'lunarYear',
                   'lunar_solar_term', 'mBzIds', 'mBzIds_2H', 'mCivetCode_000', 'mCivetCode_001', 'mCivetCode_002',
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
                   'second', 'shake', 'sj', 'sms_unread_count', 'sport_value', 'step', 'step_today', 'steps_value',
                   'storageFree', 'storageFreeNum', 'storageTotal', 'storageTotalNum', 'sunrise_time', 'sunset_time',
                   'system.date', 'system.time.ampm', 'system.time.hour1', 'system.time.hour2', 'system.time.min1',
                   'system.time.min2', 'systemVersion', 'time', 'timeZone', 'time_format', 'time_sys',
                   'touch_begin_time', 'touch_begin_x', 'touch_begin_y', 'touch_pressure', 'touch_x', 'touch_y',
                   'vibration', 'view_height', 'view_width', 'volume_level', 'volume_level_old', 'volume_type',
                   'weather', 'weather1', 'weather2', 'weather3', 'weatherRespCode', 'weather_', 'weather_city',
                   'weather_condition', 'weather_cur_temp', 'weather_description', 'weather_high_temp', 'weather_id',
                   'weather_location', 'weather_low_temp', 'weather_publish_time', 'weather_sunrise', 'weather_sunset',
                   'weather_temperature', 'weather_tmphighs', 'weather_tmplows', 'weather_wind_dir', 'weather_wind_pow',
                   'year_lunar', 'year_lunar1864', 'year_lunar_leap']

line = ''
lib_folder_name = 'lib'
assets_folder_name = 'assets'

var_alias_all = 1
var_alias = 0
var_alias_list = 0
var_alias_anti = 0
var_get_source = 0

lib_slot_xml = "$.dll"
process_xml = "$0.dll"
parse_xml = "$1.dll"
success_xml = maml_main_xml.replace(maml_file_name, 'manifest.xml')
anti_xml = "anti.xml"
config_xml = maml_main_xml.replace(maml_file_name, 'config.xml')
var_config_xml = maml_main_xml.replace(maml_file_name, 'var_config.xml')
# var_config_xml = "var_config.xml"
dev_url = 'https://www.baidu.com'

# langs_id = 0
langs_id = 4 if os.path.exists(config_xml) or os.path.exists(var_config_xml) else 2
var_persit_attr = "const" if langs_id == 0 or langs_id == 4 else "persist"


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
def getTimeSys(url):
    response = requests.get(url)
    ts = response.headers['date']
    gmt_time_obj = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    gmt_ts = time.mktime(gmt_time_obj)
    bj_internet_ts = int(gmt_ts + 8 * 3600)
    return bj_internet_ts


# 生成随机16进制数字(length:[0,16])
def randomHex(length):
    result = '0x' + hex(random.randint(0, 16 ** length)).replace('0x', '').upper()
    if len(result) < length:
        result = '0' * (length - len(result)) + result
    return result


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
def dirLib(lib_folder):
    for file in os.listdir(lib_folder):
        d = os.path.join(lib_folder, file)
        if os.path.isdir(d):
            lib.append(file.replace(lib_folder, ''))


# 获取库文件Attributes以及相应默认值
def getLib(lib_file):
    global lib_valueholder_num
    global lib_props_num
    global lib_slots_list2
    lib_valueholder_num = 0
    lib_props_num = 0

    if os.path.exists('./' + lib_folder_name + '/' + lib_file + '/' + lib_file + '.xml'):
        lib_file_name = lib_file + '.xml'
    else:
        lib_file_name = 'manifest.xml'
    lib_soup = BeautifulSoup(open('./' + lib_folder_name + '/' + lib_file + '/' + lib_file_name, encoding="utf-8"),
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
def getLibContent(lib_file_main):
    tags_lib.reverse()
    tags_str.reverse()
    tags_attr.reverse()
    lib_soup_attr.reverse()
    lib_soup_attr_def.reverse()

    if os.path.exists('./' + lib_folder_name + '/' + lib_file_main + '/' + lib_file_main + '.xml'):
        lib_file_name = lib_file_main + '.xml'
    else:
        lib_file_name = 'manifest.xml'
    lib_soup = BeautifulSoup(open('./' + lib_folder_name + '/' + lib_file_main + '/' + lib_file_name, encoding="utf-8"),
                             features="lxml-xml")

    for lib_slot in lib_soup.find_all('Slots'):
        lib_slot['id'] = randomHex(8)
        lib_slots.append(str(lib_slot))
    # for lib_slot in lib_soup.find_all('PlaceHolder'):
    # 	if lib_slot['name'] == lib_placeholder:
    # 		lib_slot.parent.append(lib_placeholder_str)
    # 		lib_slot.decompose()
    with open(lib_slot_xml, 'w', encoding='utf-8') as f0:
        if len(tags_slots):
            for j in range(len(lib_slots)):
                if len(tags_slots) < len(lib_slots):
                    tags_slots.insert(len(tags_slots), "")
                lib_soup = str(lib_soup).replace(str(lib_slots[j]), str(tags_slots[j]))
        # if len(tags_slots) > len(lib_slots):
        # 	tags_slots_str = ''
        # 	for j in range(len(tags_slots)):
        # 		tags_slots_str = tags_slots_str + str(tags_slots[j])
        # 	lib_soup = str(lib_soup).replace(str(lib_slots[0]), tags_slots_str)
        else:
            for j in range(len(lib_slots)):
                lib_soup = str(lib_soup).replace(str(lib_slots[j]), '')
        if len(lib_placeholder_str2):
            for k in range(len(lib_placeholder)):
                lib_soup = str(lib_soup).replace(str(lib_placeholder[k]), str(lib_placeholder_str2[k]))
        f0.write(str(lib_soup))

    if lib_valueholder_num == 0:
        lib_starts_with = '$'
    else:
        lib_starts_with = ''

    with open(lib_slot_xml, 'r', encoding='utf-8') as f:
        with open(process_xml, 'w', encoding='utf-8') as f2:
            for line in f:
                for i in range(len(lib_soup_attr)):
                    if lib_valueholder_num == 0:
                        for j in range(len(tags_attr)):
                            # 改动多次 慎重
                            if tags_attr[j] is None or tags_attr[i] is None:
                                line = line.replace(lib_starts_with + lib_soup_attr[i], lib_soup_attr_def[i])
                            else:
                                line = line.replace(lib_starts_with + lib_soup_attr[i], str(tags_attr[i]))
                    else:
                        # print(lib_soup_attr, tags_attr)
                        line = line.replace(lib_starts_with + lib_soup_attr[i], tags_attr[i])
                    # print(2)
                f2.write(line)
            # print(line)

    # # 筛选name及target，并添加后缀（6位随机数）

    soup = BeautifulSoup(open(process_xml, encoding="utf-8"), features="lxml-xml")

    # 找出包含【name=""】
    for tag in soup.find_all(name=True):
        if tag.get('name') is not None and tag.get('name') != '' and tag.name != "Extra" and not str(
                tag.get('name')).startswith("$") and not str(tag.get('name')).endswith("$"):
            if tag.name == 'ValueHolder':
                if tag.get('type') != 'string':
                    var_from_xml.append(tag.get('name'))
            # elif tag.name == 'item' and eval(tag.get('default')):
            # 	var_from_xml.append(tag.get('name'))
            else:
                var_from_xml.append(tag.get('name'))

    # 找出包含【dependency=""】
    for tag in soup.find_all(dependency=True):
        if tag.get('dependency') is not None and tag.get('dependency') != '' and tag.name != "Extra" and not str(
                tag.get('dependency')).startswith("$") and not str(tag.get('dependency')).endswith("$"):
            var_from_xml.append(tag.get('dependency'))

    # 找出包含【indexName=""】
    for tag in soup.find_all(indexName=True):
        if tag.get('indexName') is not None and tag.get('indexName') != '':
            var_from_xml.append(tag.get('indexName'))

    # 找出包含【countName=""】
    for tag in soup.find_all(countName=True):
        if tag.get('countName') is not None and tag.get('countName') != '':
            var_from_xml.append(tag.get('countName'))

    # 找出包含【target=""】
    for tag in soup.find_all(target=True):
        if tag.get('target') is not None:
            for i in range(len(var_from_xml)):
                target_save = str(tag.get('target').replace('.visibility', '').replace('.animation', ''))
                if target_save != var_from_xml[i] and len(target_save) >= 0:
                    var_from_xml.append(target_save)

    # soup_dom_str = str(soup.prettify(indent_width=4)).replace('    ', '\t')

    # 整理排序 + 去除系统变量
    var_from_target = list(set(var_from_xml).difference(set(var_forbid_name)))

    # 根据元素长度排序（从长到短）
    var_from_target.sort(key=lambda x: (len(x), x), reverse=True)

    # print('var_from_target: ', var_from_target, '\n')

    soup_dom_str = str(soup.prettify(indent_width=4)).replace('    ', '\t')

    # 循环替换变量
    if var_alias_all == 1:

        if var_alias != 1:
            soup_dom_hex = randomHex(8).replace('0x', '').lower()
        else:
            soup_dom_hex = ''

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace(' name="' + str(var_from_target[i]) + '"',
                                                ' name="' + soup_dom_concat + soup_dom_hex + '"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace(' target="' + str(var_from_target[i]) + '"',
                                                ' target="' + soup_dom_concat + soup_dom_hex + '"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace(' dependency="' + str(var_from_target[i]) + '"',
                                                ' dependency="' + soup_dom_concat + soup_dom_hex + '"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace(' indexName="' + str(var_from_target[i]) + '"',
                                                ' indexName="' + soup_dom_concat + soup_dom_hex + '"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace(' countName="' + str(var_from_target[i]) + '"',
                                                ' countName="' + soup_dom_concat + soup_dom_hex + '"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace(' strPara="\'' + str(var_from_target[i]) + '\'"',
                                                ' strPara="\'' + soup_dom_concat + soup_dom_hex + '\'"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '"',
                                                '#' + soup_dom_concat + soup_dom_hex + '"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '"',
                                                '@' + soup_dom_concat + soup_dom_hex + '"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + ')',
                                                '#' + soup_dom_concat + soup_dom_hex + ')')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '+',
                                                '#' + soup_dom_concat + soup_dom_hex + '+')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '-',
                                                '#' + soup_dom_concat + soup_dom_hex + '-')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '*',
                                                '#' + soup_dom_concat + soup_dom_hex + '*')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '/',
                                                '#' + soup_dom_concat + soup_dom_hex + '/')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '%',
                                                '#' + soup_dom_concat + soup_dom_hex + '%')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '=',
                                                '#' + soup_dom_concat + soup_dom_hex + '=')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '=',
                                                '@' + soup_dom_concat + soup_dom_hex + '=')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '}',
                                                '#' + soup_dom_concat + soup_dom_hex + '}')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '}',
                                                '@' + soup_dom_concat + soup_dom_hex + '}')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '{',
                                                '#' + soup_dom_concat + soup_dom_hex + '{')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '{',
                                                '@' + soup_dom_concat + soup_dom_hex + '{')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '!',
                                                '#' + soup_dom_concat + soup_dom_hex + '!')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '!',
                                                '@' + soup_dom_concat + soup_dom_hex + '!')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '[',
                                                '#' + soup_dom_concat + soup_dom_hex + '[')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '[',
                                                '@' + soup_dom_concat + soup_dom_hex + '[')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('[#' + str(var_from_target[i]) + ']',
                                                '[#' + soup_dom_concat + soup_dom_hex + ']')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('[@' + str(var_from_target[i]) + ']',
                                                '[@' + soup_dom_concat + soup_dom_hex + ']')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + ',',
                                                '#' + soup_dom_concat + soup_dom_hex + ',')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '.',
                                                '#' + soup_dom_concat + soup_dom_hex + '.')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + ' ',
                                                '#' + soup_dom_concat + soup_dom_hex + ' ')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + ')',
                                                '@' + soup_dom_concat + soup_dom_hex + ')')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '+',
                                                '@' + soup_dom_concat + soup_dom_hex + '+')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + ',',
                                                '@' + soup_dom_concat + soup_dom_hex + ',')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '.',
                                                '@' + soup_dom_concat + soup_dom_hex + '.')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + ' ',
                                                '@' + soup_dom_concat + soup_dom_hex + ' ')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('src="' + str(var_from_target[i]) + '"',
                                                'src="' + soup_dom_concat + soup_dom_hex + '"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('"' + str(var_from_target[i]) + '.animation',
                                                '"' + soup_dom_concat + soup_dom_hex + '.animation')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('"' + str(var_from_target[i]) + '.visibility',
                                                '"' + soup_dom_concat + soup_dom_hex + '.visibility')

    # print('soup_dom_str: ', soup_dom_str, '\n')
    # 定义正则表达式，匹配形如【$*$】的全局变量
    soup_pattern = re.compile(r'\$(.*?)\$')
    soup_dom_str = re.sub(soup_pattern, r'\1', soup_dom_str)

    with open(process_xml, 'w', encoding='utf-8') as f0:
        f0.write(soup_dom_str)
    # print(soup_dom_str)

    if var_alias_anti == 1:

        var_from_target.sort(reverse=False)
        # print('var_from_target: ', var_from_target, '\n')
        alias_str = '<AntiAliasing version="1"></AntiAliasing>'
        soup = BeautifulSoup(alias_str, features="lxml-xml")
        for alias in soup.find_all('AntiAliasing'):
            for j in range(len(var_from_target)):
                alias_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[j]).encode('UTF-8')))[2:].capitalize()
                alias_dom_hex = 'm' if len(alias_dom_concat) == 8 else ''
                alias_str_new = soup.new_tag('Aliasing', initial=str(var_from_target[j]),
                                             after=str(alias_dom_concat + alias_dom_hex))
                alias.append(alias_str_new)

        with open(anti_xml, 'w', encoding='utf-8') as f0:
            f0.write(str(soup.prettify(indent_width=4)).replace('    ', '\t'))

    else:
        if os.path.exists(anti_xml): os.remove(anti_xml)

    removeLibProps(process_xml, process_xml)
    return


# 移除库文件中的Props标签
def removeLibProps(lib_remove_in, lib_remove_out):
    tree = lxml.parse(lib_remove_in)
    root = tree.getroot()
    if lib_props_num != 0:
        for Props in root.findall("Props"):
            root.remove(Props)
    elif lib_valueholder_num != 0:
        for ValueHolder in root.findall("ValueHolder"):
            root.remove(ValueHolder)
        for NameHolder in root.findall("NameHolder"):
            root.remove(NameHolder)
        for PlaceHolder in root.findall("PlaceHolder"):
            root.remove(PlaceHolder)
    tree = lxml.ElementTree(root)
    tree.write(lib_remove_out, encoding="utf-8", xml_declaration=True)
    tree_str = lxml.tostring(root, encoding='unicode').replace('<Template>', '').replace('</Template>', '').replace(
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
    soup = BeautifulSoup(open(parse_file_0, encoding="utf-8"), features="lxml-xml")
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    dev_time = getTimeSys(dev_url)
    soup_indent = str(soup.prettify(indent_width=4)).replace('\n', '').replace('$_devTime', str(dev_time))
    with open(parse_file_1, 'w', encoding='utf-8') as f0:
        f0.write(soup_indent)
    return


# 保存XML文件，minidom格式化处理
def saveXML(save_file):
    global var_split_ext
    global var_split_group
    global var_alias

    # minidom格式化

    if line != '':
        soup_indent = xml.dom.minidom.parseString(line)
        soup_dom_str = soup_indent.toprettyxml()
    # print('soup_dom_str: ?', soup_dom_str)
    else:
        soup_indent = BeautifulSoup(open(parse_xml, encoding="utf-8"), features="lxml-xml")
        soup_dom_str = str(soup_indent).replace('&amp;', '&amp;amp;')
        soup_dom_str = str(soup_indent).replace('&gt;', '&amp;gt;')
        soup_dom_str = str(soup_indent).replace('&lt;', '&amp;lt;')
    # 	soup_dom_str = soup_dom_str.replace('\t \n', '\n').replace('\n\n\t', '\n\t')
    print('\t')
    print(f"LangsId: {langs_id}")
    print(f'Root: {manifest_root}')
    soup_dom_str = soup_dom_str.replace(manifest_root, 'Lockscreen')
    soup_dom_str = soup_dom_str.replace('persist_const', var_persit_attr)

    soup = BeautifulSoup(soup_dom_str, features="lxml-xml")
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    # 去除注释
    for comment in comments:
        comment.extract()

    # 根据alias属性来判断是否混淆代码
    if soup.Lockscreen.get('compiler') == 'false':
        var_alias = 0
    else:
        var_alias = 1

    var_split_ext = 1
    var_split_group = 1

    var_split_ext = 0 if str(soup.Lockscreen.get('_splitExt')).upper() == "FALSE" or soup.Lockscreen.get(
        '_splitExt') == "0" else 1
    print(f'Root[_splitExt]: {var_split_ext}')
    var_split_group = 0 if str(soup.Lockscreen.get('_splitGroup')).upper() == "FALSE" or soup.Lockscreen.get(
        '_splitGroup') == "0" else 1
    print(f'Root[_splitGroup]: {var_split_group}')

    if manifest_root == 'Lockscreen' and langs_id != 4:

        # TextSize处理
        text_size = []
        for text in soup.find_all('TextSize'):
            text_size = text.get('value', '100').split(', ')
            for t in range(len(text_size)):
                text_size_var = soup.new_tag('Var')
                text_size_var['name'] = str(text.get('_port', 'mTextSize_')) + str(text_size[t])
                text_size_var['expression'] = f'int(sqrt({text_size[t]})*#mTextSize_Var)'
                # text_size_var['type'] = 'number'
                print(f'TextSize: {text_size_var}')
                text.insert_before(text_size_var)
            text.decompose()

        # <TextSize alias="系统字体" _port="mTextSize_" value="100,90,80,70,60,50" />
        # <Var name="mTextSize_TextSizeVal_1" expression="int(sqrt(TextSizeVal_1)*#mTextSize_Var)" type="number" />

        # DateTime自动获取
        for date_time in soup.find_all('DateTime'):
            date_time_size = str(date_time.get('size'))
            if str('"mTextSize_' + date_time_size + '"') not in str(soup):
                date_time_var = soup.new_tag('Var')
                date_time_var['name'] = 'mTextSize_' + date_time_size
                date_time_var['expression'] = f'int(sqrt({date_time_size})*#mTextSize_Var)'
                print(f'DateTimeVar: {date_time_var}')
                soup.Lockscreen.append(date_time_var)

        # Text自动获取
        for text_tag in soup.find_all('Text'):
            text_tag_size = str(text_tag.get('size'))
            if str('"mTextSize_' + text_tag_size + '"') not in str(soup):
                text_tag_var = soup.new_tag('Var')
                text_tag_var['name'] = 'mTextSize_' + text_tag_size
                text_tag_var['expression'] = f'int(sqrt({text_tag_size})*#mTextSize_Var)'
                print(f'TextVar: {text_tag_var}')
                soup.Lockscreen.append(text_tag_var)

        print('\t')

    # Var.Trigger是否为空 --04.13 //内存可优化?:Test
    for var in soup.find_all('Var'):
        if 'threshold' in str(var):
            var_contents = list(set(var.Trigger.contents))
            if var_contents == ['\n']:
                var.decompose()

    soup_dom_str = str(soup.prettify(indent_width=4)).replace('    ', '\t')

    with open(save_file, 'w', encoding='utf-8') as f0:
        f0.write(soup_dom_str)

    # 包含Var的Group数量(层级)
    # var_group = []
    # for group in soup.find_all('Group'):
    # 	var_group.append(group.find_all('Var'))
    # var_group_num = len(var_group)

    # 在Group里的Var数量
    var_str = []
    for var in soup.find_all('Var'):
        if var.parent.name == 'Group':
            var_str.append(var)
    var_str_num = len(var_str)

    # ExternalCommands的数量
    ext_com = soup.find_all('ExternalCommands')
    ext_com_num = len(ext_com)

    # VariableBinders的数量
    var_binders = soup.find_all('VariableBinders')
    var_binders_num = len(var_binders)

    if var_str_num > 0: splitVar(success_xml, success_xml)
    # if ext_com_num >= 1: splitExt(success_xml)
    if var_split_ext: splitExt(success_xml)
    if var_binders_num > 1: splitBinders(success_xml)
    preLoadVar(success_xml)
    preLoadExt(success_xml)
    if var_split_group: splitGroup(success_xml, manifest_root)

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
    var_from_xml = []

    var_alias_all = 1
    # var_alias = 1
    success_xml = maml_main_xml.replace(maml_file_name, 'manifest.xml')
    origin_xml = "source.xml"
    anti_xml = "anti.xml"
    anti_list_xml = "disable.xml"

    if var_get_source:
        shutil.copy2(success_xml, maml_main_xml.replace(maml_file_name, origin_xml))
    # shutil.copy2(success_xml, origin_xml)

    # # 筛选name及target，并添加后缀（6位随机数）

    soup = BeautifulSoup(open(success_xml, encoding="utf-8"), features="lxml-xml")
    for root in soup.find_all(True, limit=1):
        for tag in root.find_all(True, limit=1):
            comment = soup.new_string('欢迎定制锁屏：灵貓 QQ 1876461209', Comment)
            tag.insert_before(comment)
            comment = soup.new_string(
                '违规抄袭将依据《中华人民共和国民法通则》《中华人民共和国著作权法》《计算机软件保护条例》《软件产品管理办法》《侵权责任法》《中华人民共和国知识产权法》追究法律责任',
                Comment)
            tag.insert_before(comment)

    # print('Comment')

    # 找出包含【name=""】
    for tag in soup.find_all(name=True):
        if tag.get('name') is not None and tag.get('name') != '' and tag.name != "Extra" and not str(
                tag.get('name')).startswith("$") and not str(tag.get('name')).endswith("$"):
            if tag.name == 'ValueHolder':
                if tag.get('type') != 'string':
                    var_from_xml.append(tag.get('name'))
            # elif tag.name == 'item' and eval(tag.get('default')):
            # 	var_from_xml.append(tag.get('name'))
            else:
                var_from_xml.append(tag.get('name'))

    # print('Name')

    # 找出包含【dependency=""】
    for tag in soup.find_all(dependency=True):
        if tag.get('dependency') is not None and tag.get('dependency') != '' and tag.name != "Extra" and not str(
                tag.get('dependency')).startswith("$") and not str(tag.get('dependency')).endswith("$"):
            var_from_xml.append(tag.get('dependency'))

    # print('Dependency')

    # 找出包含【indexName=""】
    for tag in soup.find_all(indexName=True):
        if tag.get('indexName') is not None and tag.get('indexName') != '':
            var_from_xml.append(tag.get('indexName'))

    # print('indexName')

    # 找出包含【countName=""】
    for tag in soup.find_all(countName=True):
        if tag.get('countName') is not None and tag.get('countName') != '':
            var_from_xml.append(tag.get('countName'))

    # print('countName')

    # 找出包含【target=""】
    # for tag in soup.find_all(target=True):
    # 	if tag.get('target') is not None:
    # 		for i in range(len(var_from_xml)):
    # 			target_save = str(tag.get('target').replace('.visibility', '').replace('.animation', ''))
    # 			if target_save != var_from_xml[i] and len(target_save) >= 0:
    # 				var_from_xml.append(target_save)

    # print(var_from_xml)

    # soup_dom_str = str(soup.prettify(indent_width=4)).replace('    ', '\t')

    # 整理排序 + 去除系统变量
    var_from_target = list(set(var_from_xml).difference(set(var_forbid_name)))

    # 根据元素长度排序（从长到短）
    var_from_target.sort(key=lambda x: (len(x), x), reverse=True)

    # print(var_from_target)

    soup_dom_str = str(soup.prettify(indent_width=4)).replace('    ', '\t')

    # 循环替换变量
    if var_alias_all == 1:

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

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            # soup_dom_hex = hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
            soup_dom_str = soup_dom_str.replace(' name="' + str(var_from_target[i]) + '"',
                                                ' name="' + soup_dom_concat + soup_dom_hex + '"')

            # 替换【config.xml】内的变量
            if os.path.exists(config_xml):
                config_soup_str = config_soup_str.replace('id="' + str(var_from_target[i]) + '"',
                                                          'id="' + soup_dom_concat + soup_dom_hex + '"')

            # 替换【var_config.xml】内的变量
            if os.path.exists(var_config_xml):
                var_config_soup_str = var_config_soup_str.replace('name="' + str(var_from_target[i]) + '"',
                                                                  'name="' + soup_dom_concat + soup_dom_hex + '"')

            # 替换【var_config.xml】内的变量
            if os.path.exists(var_config_xml):
                var_config_soup_str = var_config_soup_str.replace('repeatVar="' + str(var_from_target[i]) + '"',
                                                                  'repeatVar="' + soup_dom_concat + soup_dom_hex + '"')

        # 保存【config.xml】
        if os.path.exists(config_xml):
            with open(config_xml, 'w', encoding='utf-8') as f0:
                f0.write(config_soup_str.replace('\n', ''))

        # 保存【var_config.xml】
        if os.path.exists(var_config_xml):
            with open(var_config_xml, 'w', encoding='utf-8') as f0:
                f0.write(var_config_soup_str.replace('\n', ''))

        if var_alias == 0:
            soup_dom_str = soup_dom_str.replace(manifest_root + ' ',
                                                manifest_root + ' _compiler_id="' + soup_dom_hex + '" ')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace(' target="' + str(var_from_target[i]) + '"',
                                                ' target="' + soup_dom_concat + soup_dom_hex + '"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace(' dependency="' + str(var_from_target[i]) + '"',
                                                ' dependency="' + soup_dom_concat + soup_dom_hex + '"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace(' indexName="' + str(var_from_target[i]) + '"',
                                                ' indexName="' + soup_dom_concat + soup_dom_hex + '"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace(' countName="' + str(var_from_target[i]) + '"',
                                                ' countName="' + soup_dom_concat + soup_dom_hex + '"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace(' strPara="\'' + str(var_from_target[i]) + '\'"',
                                                ' strPara="\'' + soup_dom_concat + soup_dom_hex + '\'"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '"',
                                                '#' + soup_dom_concat + soup_dom_hex + '"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '"',
                                                '@' + soup_dom_concat + soup_dom_hex + '"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + ')',
                                                '#' + soup_dom_concat + soup_dom_hex + ')')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '+',
                                                '#' + soup_dom_concat + soup_dom_hex + '+')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '-',
                                                '#' + soup_dom_concat + soup_dom_hex + '-')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '*',
                                                '#' + soup_dom_concat + soup_dom_hex + '*')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '/',
                                                '#' + soup_dom_concat + soup_dom_hex + '/')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '%',
                                                '#' + soup_dom_concat + soup_dom_hex + '%')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '=',
                                                '#' + soup_dom_concat + soup_dom_hex + '=')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '=',
                                                '@' + soup_dom_concat + soup_dom_hex + '=')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '}',
                                                '#' + soup_dom_concat + soup_dom_hex + '}')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '}',
                                                '@' + soup_dom_concat + soup_dom_hex + '}')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '{',
                                                '#' + soup_dom_concat + soup_dom_hex + '{')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '{',
                                                '@' + soup_dom_concat + soup_dom_hex + '{')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '!',
                                                '#' + soup_dom_concat + soup_dom_hex + '!')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '!',
                                                '@' + soup_dom_concat + soup_dom_hex + '!')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '[',
                                                '#' + soup_dom_concat + soup_dom_hex + '[')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '[',
                                                '@' + soup_dom_concat + soup_dom_hex + '[')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('[#' + str(var_from_target[i]) + ']',
                                                '[#' + soup_dom_concat + soup_dom_hex + ']')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('[@' + str(var_from_target[i]) + ']',
                                                '[@' + soup_dom_concat + soup_dom_hex + ']')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + ',',
                                                '#' + soup_dom_concat + soup_dom_hex + ',')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + '.',
                                                '#' + soup_dom_concat + soup_dom_hex + '.')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('#' + str(var_from_target[i]) + ' ',
                                                '#' + soup_dom_concat + soup_dom_hex + ' ')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + ')',
                                                '@' + soup_dom_concat + soup_dom_hex + ')')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '+',
                                                '@' + soup_dom_concat + soup_dom_hex + '+')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + ',',
                                                '@' + soup_dom_concat + soup_dom_hex + ',')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + '.',
                                                '@' + soup_dom_concat + soup_dom_hex + '.')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('@' + str(var_from_target[i]) + ' ',
                                                '@' + soup_dom_concat + soup_dom_hex + ' ')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('src="' + str(var_from_target[i]) + '"',
                                                'src="' + soup_dom_concat + soup_dom_hex + '"')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('"' + str(var_from_target[i]) + '.animation',
                                                '"' + soup_dom_concat + soup_dom_hex + '.animation')

        for i in range(len(var_from_target)):
            if var_alias == 1:
                soup_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[i]).encode('UTF-8')))[2:].capitalize()
                soup_dom_hex = 'm' if len(soup_dom_concat) == 8 else ''
            else:
                soup_dom_concat = str(var_from_target[i]) + '_'
            soup_dom_str = soup_dom_str.replace('"' + str(var_from_target[i]) + '.visibility',
                                                '"' + soup_dom_concat + soup_dom_hex + '.visibility')

    with open(success_xml, 'w', encoding='utf-8') as f0:
        if var_alias:
            f0.write(soup_dom_str.replace('\n', ''))
        else:
            f0.write(soup_dom_str)

    if var_alias == 1:

        var_from_target.sort(reverse=False)
        # print('var_from_target: ', var_from_target, '\n')
        alias_str = '<AntiAliasing version="1"></AntiAliasing>'
        soup = BeautifulSoup(alias_str, features="lxml-xml")
        for alias in soup.find_all('AntiAliasing'):
            for j in range(len(var_from_target)):
                alias_dom_concat = 'm' + hex(zlib.crc32(str(var_from_target[j]).encode('UTF-8')))[2:].capitalize()
                alias_dom_hex = 'm' if len(alias_dom_concat) == 8 else ''
                alias_str_new = soup.new_tag('Aliasing', initial=str(var_from_target[j]),
                                             after=str(alias_dom_concat + alias_dom_hex))
                alias.append(alias_str_new)

        with open(anti_xml, 'w', encoding='utf-8') as f0:
            f0.write(str(soup.prettify(indent_width=4)).replace('    ', '\t'))

    else:
        if os.path.exists(anti_xml): os.remove(anti_xml)

    if count <= 1 and var_alias_list == 1:

        alias_list = '<DisableAliasingList></DisableAliasingList>'
        soup = BeautifulSoup(alias_list, features="lxml-xml")
        for anti_list in soup.find_all('DisableAliasingList'):
            for l in range(len(var_forbid_name)):
                alias_list_str = soup.new_tag('DisableAliasing', attrs={'name': str(var_forbid_name[l])})
                print(alias_list_str)
                anti_list.append(alias_list_str)
        with open(anti_list_xml, 'w', encoding='utf-8') as f0:
            f0.write(str(soup.prettify(indent_width=4)).replace('    ', '\t'))

    return


# 主程序
dirLib(lib_folder_name)
parseXML(maml_main_xml, parse_xml)
soup = BeautifulSoup(open(parse_xml, encoding="utf-8"), features="lxml-xml")

# 输出根标签
for root in soup.find_all(True, limit=1):
    manifest_root = str(root.name)

# globalPersist变量排除
for global_persist in soup.find_all(globalPersist=True):
    print(f"globalPersist: {global_persist['name']}")
    var_forbid_name.append(str(global_persist['name']))

# <GlVar name="mGlobalVar" globalPersist="true" />
# <Import name="mGlobalVar" globalPersist="true" />

# 输出除Lockscreen外的所有标签 
# re.compile("^(?!.*Lockscreen)^(?!.*Widget)^(?!.*Icon)")

for tag in soup.find_all(True):

    # 匹配库文件标签

    for i in range(len(lib)):

        if tag.name == lib[i] and tag.get('card') != 'Almanac' and tag.get('card') != 'Constellations' and tag.get(
                'card') != 'BigEvent':

            # 检测【disabled】属性是否存在，若存在则删除标签，并重新写入soup

            if str(tag.get('disabled')).upper() == 'TRUE' or tag.get('disabled') == '1':

                print(f'disabled: {tag}')
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
                    getLibContent(lib[i])

                # for placeholder in tag.find_all(True):
                # 	if placeholder.name == str(lib_placeholder):
                # 		print(placeholder.name, '\n')
                # 		print(placeholder, '\n')

                # 		for p in placeholder.contents:
                # 			lib_placeholder_str += str(placeholder.contents[p])

                # print('l_lib: ',len(lib_slots))
                # print('l_tags: ',len(tags_slots), '\n')
                # print('lib_slots: ', lib_slots, '\n')
                # print('tags_slots: ', tags_slots, '\n')

# 重新解析XML
soup = BeautifulSoup(open(parse_xml, encoding="utf-8"), features="lxml-xml")
for name_exp in soup.find_all(nameExp=True):
    print(f"nameExp[{randomHex(8)}]: {str(name_exp)}")
dev_time = getTimeSys(dev_url)
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

# 创建assets文件夹
if not os.path.exists(assets_folder_name):
    os.makedirs(assets_folder_name)

# 遍历每个lib文件夹
for lib_folder in tags_lib:
    src_folder = os.path.join('lib', lib_folder)
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

removeEmpty(assets_folder_name)
cleanCache()
getAlias()

# print('lib: ',lib, '\n')
# print('tags_lib: ',tags_lib, '\n')
# print('tags_str: ',tags_str, '\n')
# print('tags_attr: ',tags_attr, '\n')
# print('lib_soup_attr: ',lib_soup_attr, '\n')
# print('lib_soup_attr_def: ',lib_soup_attr_def, '\n')
# print('lib_soup_str: ',lib_soup_str, '\n')

end_time = time.time()  # 记录结束时间
run_time = f'{(end_time - start_time):.2f}'  # 计算运行时间

maml_size = os.path.getsize(maml_main_xml) / 1024  # 转换为KB
manifest_size = os.path.getsize(success_xml) / 1024  # 转换为KB
compress_rate = f'{(maml_size / manifest_size * 100):.2f}%'
print(f"Done, Script Run Time: {run_time}秒, CompressRate: {compress_rate}")
log_message = f"Script Run Time: {run_time} seconds, <CompressRate value=\"{compress_rate}\" count=\"{count}\" dev_time=\"{dev_time}\" />"
logging.info(log_message)

# 连接到数据库
conn = sqlite3.connect('counter.db')

conn.execute("INSERT INTO counter (count, source, compress_rate, run_time, dev_time) VALUES (?, ?, ?, ?, ?)",
             (count, maml_main_xml, compress_rate, run_time, dev_time))
conn.commit()

# 关闭数据库连接
conn.close()
