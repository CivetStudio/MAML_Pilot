import math
import random
import time
import datetime
from dev.Refactor.Func.formatDate import formatDate


def eq(x, y):
    """
    x==y（x 等于 y，结果为 1，否则为 0）
    """
    return 1 if x == y else 0


def ne(x, y):
    """
    x!=y（x 不等于 y，结果为 1，否则为 0）
    """
    return 1 if x != y else 0


def ge(x, y):
    """
    x>=y（x 大于等于 y，结果为 1，否则为 0）
    """
    return 1 if x >= y else 0


def gt(x, y):
    """
    x>y（x 大于 y，结果为 1，否则为 0）
    """
    return 1 if x > y else 0


def le(x, y):
    """
    x<=y（x 小于等于 y，结果为 1，否则为 0）
    """
    return 1 if x <= y else 0


def lt(x, y):
    """
    x<y（x 小于 y，结果为 1，否则为 0）
    """
    return 1 if x < y else 0


def not_(x):
    """
    逻辑非；x=0，not(x) 结果为 1；x=1，not(x) 结果为 0
    """
    return 1 if x == 0 else 0


def ifelse(*args):
    """
    如果某个参数为 True，则返回该参数对应的下一个参数值，如果所有参数都为 False，则返回最后一个参数值
    """
    if len(args) % 2 == 0:
        # 如果参数数量是偶数，最后一个参数作为默认值
        return str(args[-1])

    for i in range(0, len(args) - 1, 2):
        if args[i]:
            return str(args[i + 1])
    return str(args[-1])


def concat(*args):
    """
    可以拼接字符串；'qwe'+'rty' 结果为 'qwerty'
    """
    return ''.join(map(str, args))


def eqs(string1, string2):
    """
    字符串比较函数，如：string1 和 string2 结果一致时，eqs(string1, string2) 结果为 1 ，否则为 0
    """
    return 1 if string1 == string2 else 0


def sin(x):
    """
    返回角度 x（弧度制）的正弦值
    """
    return math.sin(x)


def cos(x):
    """
    返回角度 x（弧度制）的余弦值
    """
    return math.cos(x)


def tan(x):
    """
    返回角度 x（弧度制）的正切值
    """
    return math.tan(x)


def asin(x):
    """
    返回 x 的反正弦值，结果在 -π/2 到 π/2 之间
    """
    return math.asin(x)


def acos(x):
    """
    返回 x 的反余弦值，结果在 0 到 π 之间
    """
    return math.acos(x)


def atan(x):
    """
    返回 x 的反正切值，结果在 -π/2 到 π/2 之间
    """
    return math.atan(x)


def sinh(x):
    """
    返回 x 的双曲正弦值
    """
    return math.sinh(x)


def cosh(x):
    """
    返回 x 的双曲余弦值
    """
    return math.cosh(x)


def sqrt(x):
    """
    返回 x 的平方根
    """
    return math.sqrt(x)


# def len(num):
#     """
#     获取变量和字符串位数
#     """
#     return len(str(num))


def digit(num, pos):
    """
    取给定数字的第几位
    """
    return int(str(num)[-pos])


def substr(string, start, length):
    """
    substr('今天真热啊',1,2) = '天真'
    """
    return string[start:start + length]


def strIsEmpty(string):
    """
    判断字符串变量是否为空
    """
    return 1 if string == '' else 0


def isnull(num):
    """
    判断变量是否为空
    """
    return 1 if num is None else 0


def ceil(x):
    """
    向上取整
    """
    return math.ceil(x)


def rand():
    """
    取 0 到 1 之间的随机数
    """
    return random.random()


def strStartsWith(string_a, string_b):
    """
    判断字符串是否是某字符串开头，是则为 1，不是则为 0
    """
    return 1 if string_a.startswith(string_b) else 0


def strEndsWith(string_a, string_b):
    """
    判断字符串是否是某字符串结束，是则为 1，不是则为 0
    """
    return 1 if string_a.endswith(string_b) else 0


def strIndexOf(string_a, string_b):
    """
    字符 string_b 第一次出现在字符串 string_a 中的位置
    """
    return string_a.find(string_b)


def strLastIndexOf(string_a, string_b):
    """
    字符 string_b 最后出现在字符串 string_a 中的位置
    """
    return string_a.rfind(string_b)


def strContains(string_a, string_b):
    """
    字符串 string_a 是否包含字符 string_b
    """
    return 1 if string_b in string_a else 0


def strReplaceAll(string_a, string_b, string_c):
    """
    用 string_c 替换 string_a 中所有的 string_b
    """
    return string_a.replace(string_b, string_c)


def preciseeval(string_a, digits):
    """
    计算字符串的值，并精确到小数点后 digits 位
    """
    return round(eval(string_a), digits)


def formatFloat(string, num):
    """
    格式化小数点后 num 位，并转换成字符串
    """
    return format(num, string)


def strMatches(string, regex):
    """
    正则表达式
    """
    import re
    return 1 if re.match(regex, string) else 0


def strTrim(string):
    """
    裁切字符串的开头和尾部的空格、制表、回车符
    """
    return string.strip()


def strReplaceFirst(string_a, string_b, string_c):
    """
    替换第一个
    """
    return string_a.replace(string_b, string_c, 1)


def strToLowerCase(string):
    """
    转换成小写
    """
    return string.lower()


def strToUpperCase(string):
    """
    转换成大写
    """
    return string.upper()


if __name__ == '__main__':
    # 使用示例
    print(eq(5, 5))  # 输出：1
    print(ne(5, 10))  # 输出：1
    print(ge(5, 10))  # 输出：0
    print(gt(10, 5))  # 输出：1
    print(le(5, 10))  # 输出：1
    print(lt(10, 5))  # 输出：0
    print(not_(0))  # 输出：1
    print('ifelse:', ifelse(5 < 10, 'true', 'false'))  # 输出：false
    # print(ifelse(ne(0, 0), -1, le(2, 1), 3, gt(4, 3), 4, 5))
    print(concat('qwe', 'rty'))  # 输出：qwerty
    print('qwe' + 'rty')
    print(eqs('abc', 'abc'))  # 输出：1

    print('\nInside Function\n')

    # 调用 sin 函数，计算角度为 45 度的正弦值
    print(sin(math.radians(45)))  # 输出：0.7071067811865475

    # 调用 cos 函数，计算角度为 60 度的余弦值
    print(cos(math.radians(60)))  # 输出：0.5

    # 调用 tan 函数，计算角度为 30 度的正切值
    print(tan(math.radians(30)))  # 输出：0.5773502691896257

    # 调用 asin 函数，计算反正弦值
    print(math.degrees(asin(0.5)))  # 输出：30.0

    # 调用 acos 函数，计算反余弦值
    print(math.degrees(acos(0.5)))  # 输出：60.0

    # 调用 atan 函数，计算反正切值
    print(math.degrees(atan(1)))  # 输出：45.0

    # 调用 sqrt 函数，计算平方根
    print(sqrt(25))  # 输出：5.0

    # 调用 abs 函数，计算绝对值
    print(abs(-10))  # 输出：10

    # 调用 min 函数，找出两个数中的最小值
    print(min(5, 10))  # 输出：5

    # 调用 max 函数，找出两个数中的最大值
    print(max(5, 10))  # 输出：10

    # 调用 pow 函数，计算幂次方
    print(pow(2, 3))  # 输出：8

    # 调用 len 函数，获取变量和字符串位数
    # print(len(12345))  # 输出：5

    # 调用 digit 函数，取给定数字的第几位
    print(digit(12345, 2))  # 输出：4

    # 调用 substr 函数，获取字符串的子串
    print(substr('今天真热啊', 1, 2))  # 输出：天真

    # 调用 strIsEmpty 函数，判断字符串变量是否为空
    print(strIsEmpty(''))  # 输出：1

    # 调用 isnull 函数，判断变量是否为空
    print(isnull(None))  # 输出：1

    # 调用 ceil 函数，向上取整
    print(ceil(6.1))  # 输出：7

    # 调用 int 函数，向下取整
    print(int(6.9))  # 输出：6

    # 调用 round 函数，四舍五入取整
    print(round(6.5))  # 输出：7

    # 调用 rand 函数，生成随机数
    print(rand())  # 输出：随机数在 0 到 1 之间

    # 其他函数的使用示例同理

    # 示例的毫秒级时间戳
    # 使用 formatDate 函数将时间格式化成字符串
    date_format = 'yyyy/MM/dd HH:mm:ss:S N月e D aa t'
    textExp = formatDate(date_format, time_sys)
    print(textExp)  # 输出：'12:00'

    print('\t')


