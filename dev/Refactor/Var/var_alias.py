# 生成k位数随机字符串 *不可逆
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


def custom_encrypt(input_string, k=8, m='m'):
    global var_forbid_name
    var_forbid_name = []
    if input_string in var_forbid_name:
        return input_string
    else:
        encrypted_string = random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=max(k, 2))
        encrypted_string = m + ''.join(encrypted_string).capitalize()
        return encrypted_string


if __name__ == '__main__':
    var_string = '_dt'
    encode = custom_encrypt(var_string)
    print(var_string, ':', encode)
