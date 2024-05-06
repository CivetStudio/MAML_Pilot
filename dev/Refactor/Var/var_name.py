# 字母映射长字符串 *可逆
import random
import string

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
                   'notification_enable', 'preview_mode', 'connectedStatus', 'headsetName', 'headsetBatteryLevel',
                   'in_preview_mode']


def var_generator(k=4):
    import base64

    k = max(k, 2)

    # A: A0B
    def generate_mapping_table():
        mapping_table_ord = {}

        # 大写字母映射
        for i, char in enumerate(string.ascii_uppercase):
            mapped_char = char + str(i) + string.ascii_uppercase[(i + 1) % 26]
            encoded = base64.b64encode(mapped_char.encode()).decode().rstrip('=')
            mapping_table_ord[char] = encoded

        # 小写字母映射
        for i, char in enumerate(string.ascii_lowercase):
            mapped_char = char + str(i) + string.ascii_lowercase[(i + 1) % 26]
            encoded = base64.b64encode(mapped_char.encode()).decode().rstrip('=')
            mapping_table_ord[char] = encoded

        # 数字映射
        for i, char in enumerate(string.digits):
            mapped_char = char + str(i) + string.digits[(i + 1) % 10]
            encoded = base64.b64encode(mapped_char.encode()).decode().rstrip('=')
            mapping_table_ord[char] = encoded

        # 字符映射
        special_chars = "!@#$%^&*()_+-=[]{}|;:',.<>?/~"
        for i, char in enumerate(special_chars):
            mapped_char = char + str(i) + special_chars[(i + 1) % len(special_chars)]
            encoded = base64.b64encode(mapped_char.encode()).decode().rstrip('=')
            mapping_table_ord[char] = encoded

        return mapping_table_ord

    # Random String
    def generate_unique_strings(n):
        unique_strings = set()
        while len(unique_strings) < n:
            unique_strings.add(
                ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=k)))
        return list(unique_strings)

    # Check duplicates
    def check_duplicates(dictionary):
        value_set = set()
        duplicates_set = set()
        for value in dictionary.values():
            if value in value_set:
                duplicates_set.add(value)
            else:
                value_set.add(value)
        return duplicates_set

    # 输出映射表
    mapping_table_char = generate_mapping_table()

    # 生成不重复的4位字符串
    unique_values = generate_unique_strings(len(mapping_table_char))

    # 更新映射表的值
    mapping_table_f = {k: unique_values[i] for i, k in enumerate(mapping_table_char)}

    # 检查重复值
    duplicates = check_duplicates(mapping_table_f)
    if duplicates:
        # print("重复的值：", duplicates)
        var_generator(k)
    else:
        # print("没有重复的值。")
        return mapping_table_f


def custom_encrypt_old(text, step=6):
    encrypted_text = ""
    for char in text:
        char_ascii = ord(char)
        if 48 <= char_ascii <= 57:  # 数字
            encrypted_char = str((int(char) + step + 10) % 10)
        elif 65 <= char_ascii <= 90:  # 大写字母
            encrypted_char = chr((char_ascii + step - 65) % 26 + 65)
        elif 97 <= char_ascii <= 122:  # 小写字母
            encrypted_char = chr((char_ascii + step - 97) % 26 + 97)
        else:
            encrypted_char = char  # 其他字符不变
        encrypted_text += encrypted_char
    return encrypted_text


def custom_decrypt_old(text, step=6):
    decrypted_text = ""
    for char in text:
        char_ascii = ord(char)
        if 48 <= char_ascii <= 57:  # 数字
            decrypted_char = str((int(char) - step + 10) % 10)
        elif 65 <= char_ascii <= 90:  # 大写字母
            decrypted_char = chr((char_ascii - step - 65) % 26 + 65)
        elif 97 <= char_ascii <= 122:  # 小写字母
            decrypted_char = chr((char_ascii - step - 97) % 26 + 97)
        else:
            decrypted_char = char  # 其他字符不变
        decrypted_text += decrypted_char
    return decrypted_text


# 加密函数
def custom_encrypt(input_string):
    if input_string in var_forbid_name:
        encrypted_string = input_string
    else:
        encrypted_string = ''
        for char in input_string:
            encrypted_string += mapping_table.get(char, char)
    return encrypted_string


# 解密函数
def custom_decrypt(input_string):
    if input_string in var_forbid_name:
        return input_string
    else:
        decrypted_string = ''
        buffer = ''
        for char in input_string:
            buffer += char
            if buffer in reversed_mapping_table:
                decrypted_string += reversed_mapping_table[buffer]
                buffer = ''
        return decrypted_string


# 生成映射表和反映射表, 使用时请固定表以便解密
mapping_table = var_generator(2)

if mapping_table:
    reversed_mapping_table = {v: k for k, v in mapping_table.items()}


# if __name__ == '__main__':

#     # for i in range(256):
#     # print(f'i:{i}', chr(i))
#     # 48-57: 0-9
#     # 65-90: A-Z
#     # 97-122: a-z

def main():
    print("Welcome to var_name.py!")
    var_string = 'mResumeAni.1'
    encode = custom_encrypt(var_string)
    decode = custom_decrypt(encode)
    if not bool(decode == var_string):
        print(encode, decode)
    print(mapping_table)

if __name__ == "__main__":
    main()
    # XML 文件路径
    # maml_xml = '/Users/wangshilong/Desktop/导出/MAMLPilot/dev/Refactor/advance/source.xml'
    # save_xml = os.path.join(os.path.dirname(maml_xml), 'new.xml')
    # anti_xml = os.path.join(os.path.dirname(maml_xml), 'anti.xml')
    # var_forbid_name = ['']
    # refactor(maml_xml, 0, var_forbid_name, save_xml)
    # print(var_from_xml)
    # print(var_forbid_global)
else:
    # maml_xml = pyperclip.paste().strip()
    anti_xml = 'anti.xml'
