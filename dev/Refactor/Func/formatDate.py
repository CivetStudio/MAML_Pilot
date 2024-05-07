import time
import ephem
import math
from datetime import datetime, timedelta
import re

# Thanks to 'https://blog.csdn.net/weixin_42763614/article/details/103051262'


NN = ["正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
ee = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
TG = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DZ = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
SX = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
SOLAR_TERMS = ["小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"]
MMM = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二"]
E = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
EEEE = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

gz = [''] * 60  # 六十甲子表
for i in range(60):
    gz[i] = TG[i % 10] + DZ[i % 12]


def JD2date(JD, ut=0):
    return ephem.Date(JD + ut / 24 - 2415020)


def EquinoxSolsticeJD(year, angle):
    if 0 <= angle < 90:
        date = ephem.next_vernal_equinox(year)
    elif 90 <= angle < 180:
        date = ephem.next_summer_solstice(year)
    elif 180 <= angle < 270:
        date = ephem.next_autumn_equinox(year)
    else:
        date = ephem.next_winter_solstice(year)
    JD = ephem.julian_date(date)
    return JD


# 计算二十四节气
def SolarLongitude(JD):
    date = JD2date(JD)
    s = ephem.Sun(date)  # date应为UT时间
    sa = ephem.Equatorial(s.ra, s.dec, epoch=date)
    se = ephem.Ecliptic(sa)
    L = se.lon / ephem.degree / 180 * math.pi
    return L


def SolarTerms(year, angle):
    if angle > 270: year -= 1  # 岁首冬至
    if year == 0: year -= 1  # 公元0改为公元前1
    JD = EquinoxSolsticeJD(str(year), angle)  # 初值
    if angle >= 270:
        JD0 = EquinoxSolsticeJD(str(year), (angle - 90) % 360)
        if JD < JD0:  # 非年末冬至
            JD = EquinoxSolsticeJD(str(year + 1), angle)  # 转入次年
    JD1 = JD
    while True:
        JD2 = JD1
        L = SolarLongitude(JD2)
        JD1 += math.sin(angle * math.pi / 180 - L) / math.pi * 180
        if abs(JD1 - JD2) < 0.00001:
            break  # 精度小于1 second
    return JD1  # UT


def GregorianDateToSolarTerm(date):
    # 获取公历日期的年份
    year = int(date.split("-")[0])

    # 计算该年的所有节气日期
    solar_terms = {}
    for angle in range(0, 360, 15):
        JD = SolarTerms(year, angle)
        solar_date = JD2date(JD).datetime().strftime("%Y-%m-%d")
        term_name_index = int(angle / 15 + 5) % len(SOLAR_TERMS)
        term_name = SOLAR_TERMS[term_name_index]
        solar_terms[solar_date] = term_name

    # 检查输入的日期是否匹配某个节气日期
    if date in solar_terms:
        return solar_terms[date]
        # return f"公历日期 {date} 对应的节气是 {solar_terms[date]}"
    else:
        return ""
        # return "无节气"
        # return f"公历日期 {date} 不是节气日期"


def DateDiffer(JD1, JD2):
    return math.floor(JD1 + 8 / 24 + 0.5) - math.floor(JD2 + 8 / 24 + 0.5)


def DateCompare(JD1, JD2):  # 输入ut，返回ut+8的比较结果
    if DateDiffer(JD1, JD2) >= 0:
        return True  # JD1 >= JD 2
    else:
        return False


def findSZY(JD, shuoJD):  # 查找JD所在的农历月份
    szy = -1
    for szy_i in range(len(shuoJD)):
        if DateCompare(JD, shuoJD[szy_i]):
            szy += 1  # date所在的阴历月序，起冬至朔
    return szy


def findDZS(year):  # 寻找年前冬至月朔日
    if year == 1: year -= 1  # 公元元年前冬至在公元前1年
    dz = ephem.next_solstice((year - 1, 12))  # 年前冬至
    jd = ephem.julian_date(dz)
    # 可能的三种朔日
    date1 = ephem.next_new_moon(JD2date(jd - 0))
    jd1 = ephem.julian_date(date1)
    date2 = ephem.next_new_moon(JD2date(jd - 29))
    jd2 = ephem.julian_date(date2)
    date3 = ephem.next_new_moon(JD2date(jd - 31))
    jd3 = ephem.julian_date(date3)
    if DateCompare(jd, jd1):  # 冬至合朔在同一日或下月
        return date1
    elif DateCompare(jd, jd2) and (not DateCompare(jd, jd1)):
        return date2
    elif DateCompare(jd, jd3):  # 冬至在上月
        return date3


def LunarCalendar(nian, lunar_type=1):  # type=1时截止到次年冬至朔，=0时截止到次年冬至朔次月
    dzs = findDZS(nian)
    shuo = dzs  # 计算用朔，date格式
    shuoJD = [ephem.julian_date(dzs)]  # 存储ut+8 JD，起冬至朔
    next_dzsJD = ephem.julian_date(findDZS(nian + 1))  # 次年冬至朔
    lunar_i = -1  # 中气序，从0起计
    j = -1  # 计算连续两个冬至月中的合朔次数，从0起计
    zry = 0
    flag = False
    # 查找所在月及判断置闰
    while not DateCompare(shuoJD[j + lunar_type], next_dzsJD):  # 从冬至月起查找，截止到次年冬至朔
        lunar_i += 1
        j += 1
        shuo = ephem.next_new_moon(shuo)  # 次月朔
        shuoJD.append(ephem.julian_date(shuo))
        # 查找本月中气，若无则置闰
        if j == 0: continue  # 冬至月一定含中气，从次月开始查找
        angle = (-90 + 30 * lunar_i) % 360  # 本月应含中气，起冬至
        qJD = SolarTerms(nian, angle)
        # 不判断气在上月而后气在后月的情况，该月起的合朔次数不超过气数，可省去
        if DateCompare(qJD, shuoJD[j + 1]) and flag is False:  # 中气在次月，则本月无中气
            zry = j + 1  # 置闰月
            lunar_i -= 1
            flag = True  # 仅第一个无中气月置闰
    # 生成农历月序表
    ymb = []
    for k in range(len(shuoJD)):
        ymb.append(NN[(k - 2) % 12])  # 默认月序
        if j + lunar_type == 13:  # 仅12次合朔不闰，有闰时修改月名
            if k + 1 == zry:
                ymb[k] = '闰' + NN[(k - 1 - 2) % 12]
            elif k + 1 > zry:
                ymb[k] = NN[(k - 1 - 2) % 12]
    return ymb, shuoJD  # 月名表，合朔JD日期表


def PerpetualCalendar(year, month=0):  # 万年历（农历及公历对照），不指定月份时输出全年
    if year == 0: return print('不存在公元0年')
    ymb, shuoJD = LunarCalendar(year, 0)
    if DateCompare(ephem.julian_date((year, 12, 31)), shuoJD[-2] + 29):
        ymb1, shuoJD1 = LunarCalendar(year + 1)
        ymb = ymb[:-2] + ymb1[:2]
        shuoJD = shuoJD[:-2] + shuoJD1[:3]
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days[1] = 29 if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0 else 28
    if year < 1582 and year % 4 == 0: days[1] = 29
    week = ['一', '二', '三', '四', '五', '六', '日', ]
    for j in range(12):
        if month != 0 and j + 1 != month: continue
        print('【' + str(year) + '年 ' + str(j + 1) + '月  日历】')
        ysJD = ephem.julian_date((year, j + 1))
        szy = findSZY(ysJD, shuoJD)  # 公历岁首对应的农历月
        ysRQ = DateDiffer(ysJD, shuoJD[szy])  # 每月1日的农历日期
        yue0 = DateDiffer(shuoJD[szy + 1], shuoJD[szy])
        yue1 = DateDiffer(shuoJD[szy + 2], shuoJD[szy + 1])
        blank = int((ysJD + 0.5) % 7)
        flag = False
        for row in range(6 * 2 + 1):
            if row % 2 == 1 and flag: break
            for k in range(7):
                if row % 2 == 1:  # 公历行
                    day = row // 2 * 7 + k - blank + 1
                    if year == 1582 and j == 9:
                        if day > 4: day += 10
                elif row != 0:  # 农历行
                    if row == 2 and k >= blank or row > 2:
                        rqx = ysRQ + row // 2 * 7 - 7 + k - blank
                        if rqx == 0:
                            rq = ymb[szy]
                        elif 0 < rqx < yue0:
                            rq = ee[rqx]
                        elif rqx == yue0:
                            rq = ymb[szy + 1]
                        elif yue0 < rqx < yue0 + yue1:
                            rq = ee[rqx - yue0]
                        elif rqx == yue0 + yue1:
                            rq = ymb[szy + 2]
                        elif rqx > yue0 + yue1:
                            rq = ee[rqx - yue0 - yue1]
                # 输出排版
                if row == 0:
                    print(" {:<5}".format(week[k]), end='')
                elif row == 1 or row == 2:  # 首行
                    if k == 0:
                        print('       ' * blank, end='')
                    if row == 1 and k >= blank:
                        print(" {:<6d}".format(day), end='')
                    if row == 2 and k >= blank:
                        print("{0:{1}<3}".format(rq, '\u3000'), end=' ')
                else:
                    if row % 2 == 1 and row != 1:
                        if day <= days[j]:
                            print(" {:<6d}".format(day), end='')
                        else:
                            flag = True
                            break
                    if row % 2 == 0 and row != 0 and row != 2:
                        if year == 1582 and j == 9 and day > days[j]: break
                        print("{0:{1}<3}".format(rq, '\u3000'), end=' ')
                        if row // 2 * 7 + k - blank - 6 >= days[j]: break
            print()
        print()


class SolarToLunarConverter:
    def __init__(self):

        self.A = ''
        self.G = ''
        self.Y = ''
        self.YY = ''
        self.yy = ''
        self.yyyy = ''
        self.M = ''
        self.MM = ''
        self.MMM = ''
        self.MMMM = ''
        self.N = ''
        self.NN = ''
        self.NNN = ''
        self.NNNN = ''
        self.D = ''
        self.d = ''
        self.dd = ''
        self.e = ''
        self.ee = ''
        self.t = ''
        self.E = ''
        self.EE = ''
        self.EEE = ''
        self.EEEE = ''
        self.EEEEE = ''
        self.H = ''
        self.h = ''
        self.HH = ''
        self.hh = ''
        self.I = ''
        self.II = ''
        self.m = ''
        self.mm = ''
        self.mmm = ''
        self.mmmm = ''
        self.s = ''
        self.ss = ''
        self.sss = ''
        self.ssss = ''
        self.S = ''
        self.U = ''
        self.a = ''
        self.aa = ''
        self.Z = ''
        self.ZZ = ''
        self.ZZZ = ''
        self.ZZZZ = ''
        self.ZZZZZ = ''
        self.zzzz = ''

        # 收集所有的 self.xxx 属性作为数组
        self.property_names = [name for name in dir(self) if not name.startswith('__') and name != 'property_names']

    def Solar2LunarCalendar(self, date, date_local, timestamp_ms=None):  # 默认输入ut+8时间
        if date[0] == '0':
            return '不存在公元0年'

        JD = ephem.julian_date(date) - 8 / 24  # ut
        year, month, day = JD2date(JD, 8).triple()

        # 判断所在年
        dzs = findDZS(year)  # 本年冬至朔
        next_dzs = findDZS(year + 1)  # 次年冬至朔
        this_dzsJD = ephem.julian_date(dzs)
        next_dzsJD = ephem.julian_date(next_dzs)
        nian = year  # 农历年
        if DateCompare(JD, next_dzsJD):  # 该日在次年
            nian += 1
        if not DateCompare(JD, this_dzsJD):  # 该日在上年
            nian -= 1

        # 判断所在月
        ymb, shuoJD = LunarCalendar(nian)
        szy = findSZY(JD, shuoJD)

        # 判断节气月
        if year < 0:
            year += 1

        jqy, jqr = JD2date(SolarTerms(year, month * 30 + 255), 8).triple()[1:]
        if int(jqy) != month:
            month -= (int(jqy) - month)
        if day >= int(jqr):
            ygz = gz[(year * 12 + 12 + month) % 60]
        else:
            ygz = gz[(year * 12 + 11 + month) % 60]

        # 以正月开始的年干支
        if szy < 3:
            nian -= 1  # 正月前属上年
        if nian < 0:
            nian += 1
        ngz = gz[(nian - 4) % 60]
        rgz = gz[math.floor(JD + 8 / 24 + 0.5 + 49) % 60]
        rq = DateDiffer(JD, shuoJD[szy])  # 月内日期

        jq = GregorianDateToSolarTerm(date)

        import dev.Refactor.Func.ganzhi as ganzhi
        from typing import Union

        self.A = SX[(nian - 1900) % 12]
        self.G = '公元'
        self.Y = number_to_chinese(year)
        self.YY = ngz
        self.yy = str(year)[-2:]
        self.yyyy = year
        self.M = int(month)
        self.MM = convert_to_digit(month)
        self.MMM = MMM[month]
        self.MMMM = MMM[month] + '月'
        self.N = ymb[szy][:-1]
        self.NN = ygz
        self.NNN = ymb[szy] + ee[rq] + ' ' + jq if jq else ymb[szy] + ee[rq]
        self.NNNN = self.NNN
        self.D = day_of_year(date)
        self.d = int(day)
        self.dd = convert_to_digit(int(day))
        self.e = ee[rq]
        self.ee = rgz
        self.t = jq
        self.E = E[get_weekday(date_local)]
        self.EE = self.E
        self.EEE = self.E
        self.EEEE = EEEE[get_weekday(date_local)]
        self.EEEEE = self.E.replace('周', '')
        self.H = int(date_local.hour)
        self.h = int(convert_to_hour12(self.H))
        self.HH = convert_to_digit(self.H)
        self.hh = convert_to_digit(self.h)
        self.I = ganzhi.get_time_gan_zhi(date_local)[1:]
        self.II = ganzhi.get_time_gan_zhi(date_local)
        self.m = int(date_local.minute)
        self.mm = convert_to_digit(self.m)
        self.mmm = convert_to_digit(self.m, 3)
        self.mmmm = convert_to_digit(self.m, 4)
        self.s = int(date_local.second)
        self.ss = convert_to_digit(self.s)
        self.sss = convert_to_digit(self.s, 3)
        self.ssss = convert_to_digit(self.s, 4)
        self.S = str(int(timestamp_ms))[-3:]
        # self.S = datetime.now().strftime('%f')[:3] if datetime.now().strftime('%H-%M-%S') == date_local.strftime('%H-%M-%S') else convert_to_digit(int((timestamp_ms % 1) * 1000), 3)
        # print(abs(int(self.S)-int(self.U)))
        self.a = '下午' if self.H > 12 else '上午'
        self.aa = get_time_description(self.H)
        self.Z = '+0800'
        self.ZZ = '+0800'
        self.ZZZ = '+0800'
        self.ZZZZ = 'GMT+08:00'
        self.ZZZZZ = '08:00'
        self.zzzz = '中国标准时间'
        eval_array = self.property_names
        eval_array.sort(key=lambda x: len(x), reverse=True)
        return eval_array


def convert_to_digit(number, k=2):
    n = f'number:0{k}'
    n = "f'{" + n + "}'"
    result = eval(n)
    if int(number) < pow(10, k-1):
        return result.split('.')[0]
    else:
        return result.split('.')[0]


def convert_to_hour12(hour):
    if hour > 12:
        return hour - 12
    elif hour == 12:
        return hour
    elif hour == 0:
        return 12
    else:
        return hour


def get_time_description(hour):
    if hour is None:
        return ""
    else:
        time_intervals = [
            {"min": 0, "max": 5, "text": "凌晨"},
            {"min": 6, "max": 11, "text": "上午"},
            {"min": 12, "max": 13, "text": "中午"},
            {"min": 14, "max": 17, "text": "下午"},
            {"min": 18, "max": 19, "text": "傍晚"},
            {"min": 20, "max": 24, "text": "晚上"}
        ]
        for interval in time_intervals:
            if interval["min"] <= hour <= interval["max"]:
                return interval["text"]


def get_weekday(date_str):
    # 获取星期几（0 代表星期一，1 代表星期二，以此类推）
    weekday = date_str.weekday()
    # 返回对应的星期几名称
    return int(weekday)


def day_of_year(date_str):
    # 将日期字符串转换为datetime对象
    date = datetime.strptime(date_str, "%Y-%m-%d")
    # 获取一年中的第一天
    start_of_year = datetime(date.year, 1, 1)
    # 计算日期与一年中的第一天之间的时间差
    delta = date - start_of_year
    # 返回日期是一年中的第几天（加1是因为第一天的索引为0）
    return delta.days + 1


def number_to_chinese(number):
    chinese_numerals = ["〇", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
    # chinese_units = ["", "十", "百", "千", "万"]

    result = ""
    str_number = str(number)
    length = len(str_number)

    for n_i in range(length):
        digit = int(str_number[n_i])
        unit_index = length - n_i - 1

        # 处理特殊情况：零
        if digit == 0:
            if unit_index == 0 or (unit_index > 0 and int(str_number[n_i + 1]) != 0):
                result += chinese_numerals[digit]
            continue

        # 添加数字
        result += chinese_numerals[digit]

    return result


def date_to_timestamp(date_str):
    # 使用strptime方法将日期字符串解析为datetime对象
    date_time_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    # 使用timestamp方法将datetime对象转换为时间戳
    timestamp_ms = date_time_obj.timestamp() * 1000  # 将秒级时间戳转换为毫秒级时间戳
    return int(timestamp_ms)


def timestamp_to_date(timestamp_ms):
    # 将毫秒级时间戳转换为秒级时间戳
    timestamp_ms = int(timestamp_ms)
    timestamp_sec = timestamp_ms / 1000.0
    # 使用fromtimestamp方法将秒级时间戳转换为日期时间对象
    date_time_obj = datetime.fromtimestamp(timestamp_sec)
    # 将日期时间对象格式化为指定的日期格式（例如：2024-05-20）
    formatted_date = date_time_obj.strftime('%Y-%m-%d %H:%M:%S')
    # formatted_hour = date_time_obj.strftime('%H')
    return formatted_date


def formatDate(eval_re, timestamp_ms):

    # 示例：将日期转换为毫秒级时间戳
    # date_str = "2024-04-10 13:01:12"  # 日期字符串
    # timestamp_ms = date_to_timestamp(date_str)

    # 示例：将毫秒级时间戳转换为日期格式
    # timestamp_ms = 1712678400000  # 毫秒级时间戳
    # timestamp_ms = int(time.time() * 1000)
    # print("时间戳:", timestamp_ms)

    timestamp_ms = int(timestamp_ms)
    date_str = timestamp_to_date(timestamp_ms)[:10]
    date_local = timestamp_to_date(timestamp_ms)
    date_local = datetime.strptime(date_local, "%Y-%m-%d %H:%M:%S")
    # print("公历日期:", date_local)

    converter = SolarToLunarConverter()
    eval_array = converter.Solar2LunarCalendar(date_str, date_local, timestamp_ms)
    # print(eval_re)

    # 定义正则表达式模式
    pattern = r'(?=(A|G|YY|Y|yyyy|yy|MMMM|MMM|MM|M|NNNN|NNN|NN|N|dd|d|D|ee|e|t|EEEEE|EEEE|EEE|EE|E|HH|H|hh|h|II|I|mmmm|mmm|mm|m|ssss|sss|ss|s|S|aa|a|ZZZZZ|ZZZZ|ZZZ|ZZ|Z|zzzz))\1(.*?)'
    # G|YYYY|YY|yyyy|yyy|yy|MMM|MM|M|dd|d|D|HH|H|hh|h|mmmm|mmm|mm|m|ssss|sss|ss|s|S|NNNN|NNN|NN|N|EEEE|EEE|EE|E|ee|e|ZZZZZ|ZZZZ|ZZZ|Z|zzzz|ssss|sss|ss|s|II|I|A|aa|a|t

    # 要匹配的字符串
    input_string = eval_re

    # 使用re模块进行匹配
    matches = re.findall(pattern, input_string)

    # 将结果处理为数组
    result = [match[0] for match in matches]

    # 打印结果数组
    # print(result)

    for x in range(len(result)):
        try:
            eval_final = str(eval('converter.' + result[x]))
            eval_re = eval_re.replace(result[x], eval_final)
        except Exception:
            eval_final = ''
        # print(eval_array[x], eval('converter.' + eval_array[x]))

    # for x in range(len(eval_array)):
    #     eval_final = str(eval('converter.' + eval_array[x]))
    #     eval_re = eval_re.replace(eval_array[x], eval_final)
    #     # print(eval_array[x], eval('converter.' + eval_array[x]))

    return eval_re


if __name__ == '__main__':

    fps = 240
    fps = 1

    for i in range(fps):
        # print(i, end='', flush=True)  # 使用 flush=True 实时刷新输出

        time_sys = time.time() * 1000
        # print(time_sys)
        format_date = '''
        HH:mm:ss:S
        yyyy年M月d日
        生肖:      A
        干支年: YY年
        干支月: NN月
        干支日: ee日
        农历: N月e t
        时辰地支: II
        '''
        format_date = 'yyyy年MM月dd日 EEEE 农历NNNN\nNN月 ee日 II时'
        textExp = formatDate(format_date, time_sys)
        print(textExp)
        print(bool(type(textExp) is str))

        time.sleep(1/fps)


def Lunar2SolarCalendar(nian, date):  # 正月开始的年
    date1 = date.split('闰')[-1]
    year = nian
    yx = NN.index(date1[:-2])
    if yx + 1 > 10: year += 1  # 计算用年，起冬至朔
    if year == 0: return '不存在公元0年'
    yx = (yx + 2) % 12  # 子正转为寅正
    if "闰" in date: yx += 1
    # 查找所在月
    ymb, shuoJD = LunarCalendar(year, 0)
    szy = 0
    for ymb_i in range(len(ymb)):
        if ymb[ymb_i] == date1[:-2]:  # 按月序查找
            if ymb[ymb_i + 1] == date[:-2] or '闰' in date:
                szy += 1  # 可能为闰月（不闰则计算次月）
            break
        szy += 1
    # 获得农历日期
    try:
        rq = ee.index(date[-2:])
    except Exception as e:
        rgz = gz.index(date[-2:])
        sgz = math.floor(shuoJD[szy] + 8 / 24 + 0.5 + 49) % 60
        rq = (rgz - sgz) % 60
        if DateCompare(shuoJD[szy] + rq, shuoJD[szy + 1]):
            print('该月无' + date[-2:])
        else:
            print(date[-2:] + '为该月' + ee[rq] + '日')
    date2 = str(JD2date(shuoJD[szy] + rq, 8))[:-9]
    return '农历' + str(nian) + '年' + date + ' 为公历：' + date2

# PerpetualCalendar(2024)

# date = input('请输入日期：')
# date = "2024-04-04"
# date1 = "2016-11-29"
# date2 = "2033-9-1"  # 无中气月，一年仅得12月，不闰
# date3 = "2033-12-31"  # 冬至起的第一个无中气月，闰
# date4 = "2034-3-1"  # 冬至起的第二个无中气月，不闰
# print(Solar2LunarCalendar(date))

# print(Lunar2SolarCalendar(-1696, '十一月甲子'))
# print(Solar2LunarCalendar('-1695/1/7'))
# print(Lunar2SolarCalendar(2020, '正月初一'))
# print(Lunar2SolarCalendar(2033, '闰十一月十一'))

# # from zhdate import ZhDate
# # import datetime
# #
# # # 从阳历日期转换为农历日期对象
# # dt_date2 = datetime.datetime(2024, 4, 10)
# # date2 = ZhDate.from_datetime(dt_date2)
# # print("阳历日期:", dt_date2)
# # print("对应的农历日期:", date2)
