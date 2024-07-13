import math
import ephem
from datetime import datetime, timedelta
from typing import Union


# 天干和地支的周期表
GAN10 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]  # 十天干
ZHI12 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]  # 十二地支


# 获取当前环境的时区偏移值
def cur_time_zone_offset() -> float:
    current_time = datetime.now()
    # 获取UTC时间
    utc_time = datetime.utcnow()
    # 计算小时差
    time_zone_offset = round((current_time - utc_time).seconds / 3600.0, 2)
    # 以0.5为基准进行舍入操作:
    if time_zone_offset >= 0:
        time_zone_offset = math.floor(time_zone_offset / 0.5 + 0.5) * 0.5
    else:
        time_zone_offset = math.ceil(time_zone_offset / 0.5 - 0.5) * 0.5
    return time_zone_offset


# 计算指定本地时间的真太阳时
def calculate_true_solar_time(date_local: datetime, observer_latitude: Union[str, float] = 34.545811,
                              observer_longitude: Union[str, float] = 108.925825) -> datetime:
    """
    根据观测者的经纬度和时间，计算真太阳时。

    参数：
    observer_latitude (str): 观测者的纬度，以度为单位。
    observer_longitude (str): 观测者的经度，以度为单位。
    date_local (datetime): 观察时间

    返回：
    datetime: 调整后的真太阳时，已考虑观测者的经纬度和时区偏移量。
    """
    # 根据观测者的经纬度和时间，计算真太阳时:
    # 计算当前时区偏移time_zone_offset
    time_zone_offset = cur_time_zone_offset()
    # 将观测者的纬度和经度转换为ephem格式
    lat, lon = ephem.degrees(str(observer_latitude)), ephem.degrees(str(observer_longitude))

    # 创建一个新的观测者对象
    observer = ephem.Observer()
    observer.lat, observer.lon = lat, lon

    # 将输入的当地时间转换为ephem的Date格式
    date_0 = date_local - timedelta(hours=time_zone_offset)  # 将本地时间转换为UTC+0时间
    utc_date = ephem.Date(date_0)

    # 设置观测者的日期和时间
    observer.date = utc_date

    # 计算太阳的位置
    sun = ephem.Sun(observer)
    # 计算本地太阳正午时间（在给定日期太阳通过当地子午线的时间）
    next_noon = observer.next_transit(sun).datetime() + timedelta(hours=time_zone_offset)
    # 计算钟表正午时间
    clock_noon = next_noon.replace(hour=12, minute=0, second=0, microsecond=0)
    # 计算太阳正午和钟表正午之间的差值
    time_diff = (clock_noon - next_noon).total_seconds() / 3600.0
    # 调整本地时间以获得真太阳时(ephem通常已经考虑光行差)
    true_solar_time = date_local + timedelta(hours=time_diff)
    return true_solar_time


# 求指定日期的年份干支(年柱)
def get_year_gan_zhi(date: datetime, observer_latitude: Union[str, float, int] = 0,
                     observer_longitude: Union[str, float, int] = 0) -> str:
    startDate = datetime(2000, 2, 4, 20, 40, 24)  # 2000年立春时间
    # 如果指定了站点则计算真太阳时间:
    if observer_latitude != 0 or observer_longitude != 0: date = calculate_true_solar_time(date, observer_latitude, observer_longitude)
    diff_days = (date - startDate).days  # 计算指定日期与2000年2月4日之间的间隔天数

    # 回归年的长度：365.24218968 - 0.0000000616*(t-2000)
    day_per_year = 365.24218968 - 0.0000000616 * (diff_days / 365.24218968 / 2)  # 回归年的平均长度
    years = math.floor(diff_days / day_per_year)  # 算指定日期与2000年2月4日之间的年数

    # 2000年是庚辰年
    gan_index = (years + 6) % 10  # 加6位
    zhi_index = (years + 4) % 12  # 加4位
    gan_zhi = GAN10[gan_index] + ZHI12[zhi_index]
    return gan_zhi


# 计算指定站点在特定时间的月干支(月柱)
def get_moon_gan_zhi(date: datetime, latitude: Union[str, float] = 34.545811,
                     longitude: Union[str, float] = 108.925825) -> str:
    """
    计算指定站点在特定时间的月干支。

    参数:
    date : datetime
        观察时间
    latitude : float
        观察者的纬度（度）。默认为35度
    longitude : float
        观察者的经度（度）。默认为120度

    返回:
    str
        指定时间的月干支，范围从"甲子"到"癸亥"。
    """
    # 创建观察者的地球位置对象
    observer = ephem.Observer()
    observer.lat, observer.lon = ephem.degrees(str(latitude)), ephem.degrees(str(longitude))  # 纬度，经度,需要转换为弧度
    # 计算当前时区偏移hour_difference
    hour_difference = cur_time_zone_offset()

    # 解析日期字符串
    date_local = date
    date_0 = date_local - timedelta(hours=hour_difference)  # 将本地时间转换为UTC+0时间
    date = ephem.Date(date_0)

    # 创建观察者对象
    observer.date = date
    sun = ephem.Sun(observer)
    # 获取太阳的视黄经（转换为度）:
    equ = ephem.Equatorial(sun.ra, sun.dec, epoch=date)  # 求太阳的视赤经视赤纬（epoch设为所求时间就是视赤经视赤纬）
    ecl_v = ephem.Ecliptic(equ)  # 赤经赤纬转到黄经黄纬
    solar_longitude = (float(ecl_v.lon) * 180.0 / ephem.pi) % 360.0  # 对视黄经进行修正为0到360度的范围

    start_date = datetime(2000, 3, 5, 14, 42, 40)  # 己卯月始于3月5日 14:42:40惊蛰
    diff_days = (date_local - start_date).days
    day_per_moon = (365.24218968 - 0.0000000616 * (diff_days / 365.24218968 / 2)) / 12
    moon_num = int(diff_days / day_per_moon)  # 从己卯月开始的第几个月
    solar_longitude_mi = (int(((solar_longitude - 15) % 360) / 30.0) + 4) % 12  # 推算月支与黄经的对应关系
    moon_num_id = (moon_num + 3) % 12  # 月支序数
    t12_diff = (
                       solar_longitude_mi - moon_num_id + 12) % 12  # 修正增量值(t12_diff)=精确地支序号(solar_longitude_mi)-近似地支序号(moon_num_id)
    # 修正当solar_longitude_mi和moon_num_id分别居于头尾的偏差:
    # 如果 t12_diff 大于等于 6，表示实际差值应为负数，因此再减去12
    if t12_diff >= 6: t12_diff -= 12
    moon_num += t12_diff  # 月支序数修正
    gan_index = (moon_num + 5) % 10  # 加5位
    zhi_index = (moon_num + 3) % 12  # 加3位
    gan = GAN10[gan_index]  # 天干序列的获取
    zhi = ZHI12[zhi_index]  # 地支序列的获取
    return gan + zhi  # 月干支的返回


# 计算日的干支(日柱)
def get_day_gan_zhi(date_local: datetime, observer_latitude: Union[str, float] = 34.545811,
                    observer_longitude: Union[str, float] = 108.925825) -> str:
    start_date = datetime(1900, 1, 1, 0, 0, 0, 0)  # 日的分隔点是真太阳时0:0:0
    # 根据观测者的经纬度和时间，计算真太阳时(ephem通常已经考虑光行差):
    true_solar_time = calculate_true_solar_time(date_local, observer_latitude, observer_longitude)
    difference_in_days = (true_solar_time - start_date).days
    # 1900年1月1日是甲戌日:
    gan_index = (difference_in_days + 0) % 10  # 加0位
    zhi_index = (difference_in_days + 10) % 12  # 加10位
    gan_zhi = GAN10[gan_index] + ZHI12[zhi_index]
    return gan_zhi


# 计算时的干支(时柱)
def get_time_gan_zhi(date_local: datetime, observer_latitude: Union[str, float] = 34.545811,
                     observer_longitude: Union[str, float] = 108.925825) -> str:
    """
    根据观测者的经纬度和时间，计算真太阳时。

    参数：
    observer_latitude (str): 观测者的纬度，以度为单位。
    observer_longitude (str): 观测者的经度，以度为单位。
    date_local (datetime): 观察时间

    返回：
    datetime: 调整后的真太阳时，已考虑观测者的经纬度和时区偏移量。
    """
    # 根据观测者的经纬度和时间，计算真太阳时(ephem通常已经考虑光行差):
    true_solar_time = calculate_true_solar_time(date_local, observer_latitude, observer_longitude)
    true_solar_time = date_local
    start_time_period = datetime(1983, 12, 21, 23, 42, 15)  # 甲子月甲申日甲子时真太阳时起始点
    total_time_periods = round((true_solar_time - start_time_period).total_seconds() / 3600.0 / 2.0)  # 已经过去多少个时辰
    total_time_correction = ((((
                                       true_solar_time.hour + 1) // 2 - total_time_periods) % 12) + 12) % 12  # 子时的起点是真太阳时23:00:00
    if total_time_correction >= 6: total_time_correction -= 12
    total_time_periods += total_time_correction
    # 1983-12-21 23:42:15是甲子时:
    gan_index = (total_time_periods + 0) % 10  # 加0位
    zhi_index = (total_time_periods + 0) % 12  # 加0位
    gan_zhi = GAN10[gan_index] + ZHI12[zhi_index]
    return gan_zhi


# 使用示例:
# date_str = '2024-04-10 11:34:19'  # 示例时间
# observer_latitude, observer_longitude = '39.9', '110.8333'
# date_test = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
# moon_gan_zhi = get_moon_gan_zhi(date_test, observer_latitude, observer_longitude)
# day_gan_zhi = get_day_gan_zhi(date_test, observer_latitude, observer_longitude)
# year_gan_zhi = get_year_gan_zhi(date_test, observer_latitude, observer_longitude)
# shi_gan_zhi = get_time_gan_zhi(date_test, observer_latitude, observer_longitude)
#
# print(date_str + "中的年柱:" + year_gan_zhi)
# print(date_str + "中的月柱:" + moon_gan_zhi)
# print(date_str + "中的日柱:" + day_gan_zhi)
# print(date_str + "中的时柱:" + shi_gan_zhi)

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
