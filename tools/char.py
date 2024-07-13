import random
import sys


# 加密函数
def encrypt_number(number):
    # encrypted = 0
    mod_val = 1000000007

    # 简单的置换操作
    encrypted = (number * 123456789) % mod_val

    return encrypted


# 数字映射为3位数的字母
def map_to_letters(number):
    letters = ""

    # 字母表
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    # 将数字分为三个部分，每个部分映射为一个字母
    part1 = int(number / (26 * 26)) % 26
    part2 = int(number / 26) % 26
    part3 = int(number % 26)
    print("{:02d} {:02d} {:02d}".format(part1, part2, part3))

    # 根据数字映射为字母
    letters += alphabet[part1]
    letters += alphabet[part2].upper()
    letters += alphabet[part3]

    return letters


# 数字映射为3位数的字母
def map_to_letters_reverse(number):
    letters = ""

    # 字母表
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    # 将数字分为三个部分，每个部分映射为一个字母
    part1 = (26 - int(number / (26 * 26)) % 26) % 26
    part2 = (26 - int(number / 26) % 26) % 26
    part3 = (26 - int(number % 26)) % 26
    print("{:02d} {:02d} {:02d}".format(part1, part2, part3))

    # 根据数字映射为字母
    letters += alphabet[part1]
    letters += alphabet[part2].upper()
    letters += alphabet[part3].upper()

    return letters


# 测试
original_number = 52086045
original_number = int(random.random() * 999999999999)
original_char = '5136f8e9117ceb89'
translation_table = str.maketrans('abcdef', '012345')
original_char = original_char.translate(translation_table)
print(original_char)
original_number = int(original_char[:8])
# original_number = 51956522
# original_number = 1323365097
encrypted_number = encrypt_number(original_number)
mapped_letters = map_to_letters(encrypted_number)
reversed_letters = map_to_letters_reverse(encrypted_number)
combined_letters = str(mapped_letters) + str(encrypted_number) + \
                   str(reversed_letters) + str(int(encrypted_number % 26))

print('Original Number:', original_number)
print('Encrypted Number:', encrypted_number)
print('Mapped Letters:', mapped_letters)
print('Combined Letters:', combined_letters)
