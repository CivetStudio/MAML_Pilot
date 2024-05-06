import re
from bs4 import BeautifulSoup
from lxml import etree
from dev.Refactor.functions import *
from dev.Refactor.refactor import get_xml_variable
from decimal import Decimal, ROUND_DOWN

orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


BeautifulSoup.prettify = prettify

xml_content = """
<MAML>
    
    <!-- 数字类型 -->
    <Var name="numVar" type="number[]" const="true" expression="" values="100,150,500,550,800,850"/>
    <!-- 文本类型；注意：文本类型 必须要 包含 expression="''" 属性 -->
    <Var name="strVar" type="string[]" const="true" expression="''" values="'水瓶座','双鱼座','白羊座','金牛座','双子座','巨蟹座','双子座','处女座','天秤座','天蝎座','射手座','摩羯座'"/>
        
    <C_Array count="3" indexName="_i" >
        
        <Var _c="1" name="c_a" type="number[]" values="187, 64, 61, 20, 9" />
        <Var _c="1" name="c_color" type="string[]" values="'#ffffff', '#000000', '#ff00ff'" />
        <Var _c="1" name="c_string" type="string[]" values="'aaa', 'bbb', 'ccc'" />
        
        <Text x="{#c_a[#_i]}" y="100+200*#_i" color="{@c_color[#_i]}" size="{#c_a[#_i]}" text="{@strVar[#_i]}" visibility="1" />
        <Button x="{#c_a[#_i]}" y="100+200*#_i" w="400" h="100" visibility="1">
            <Triggers>
                <Trigger action="click">
                    <VariableCommand persist="true" name="id_{#_i+1}" expression="not(#id_#_i)" type="number" />
                </Trigger>
            </Triggers>
        </Button>
        
    </C_Array>
    
</MAML>
    
"""

comment_content = """

    <!--

    <C_Array begin="0" end="1" indexName="_j" >
        
		<Var name="mEyesAni_t.#_i" >
			<VariableAnimation delay="{#_i*720}" >
				<AniFrame value="0" time="0" />
				<AniFrame easeType="CubicEaseOut" varSpeedFlag="CubicFun_Out" value="#_dt_rw" time="300" />
				<AniFrame easeType="CubicEaseOut" varSpeedFlag="CubicFun_Out" value="#_dt_rw" time="1700" />
				<AniFrame easeType="BackEaseOut" varSpeedFlag="BackFun_Out" value="0" time="2000" />
				<AniFrame easeType="BackEaseOut" varSpeedFlag="BackFun_Out" value="0" time="5000" />
			</VariableAnimation>
		</Var>
		
        <Button x="500+#_i*500" y="600" w="900" h="900" visibility="300" >
            <Triggers>
                <Trigger action="up" >
                    <VariableCommand name="nnn_#_i" expression="300*#_i" type="number" />
                </Trigger>
            </Triggers>
        </Button>

        <Text x="13+#Ani_#_j*13" y="13+#_j*13" color="#ff0000" size="13" text="Ani_#_j" />
        <VariableCommand name="test_#index" expression="#index" type="number" />

    </C_Array>
    
        <C_Array count="4" indexName="index">
        </C_Array>
    -->
    
"""


def c_array_bak(code):
    soup = BeautifulSoup(code, 'lxml-xml')
    for array in soup.find_all('C_Array'):
        # 搜索替换 【#_i】 为 count 循环后的数字
        tags_index = str('#' + array.get('indexName'))
        tags_count = int(array.get('count'))
        tags = array.find_all('Button')
        for i in range(tags_count):
            for t in range(len(tags)):
                soup_child = BeautifulSoup(str(tags[t]), 'lxml-xml')
                new_group = soup_child.new_tag('Group')
                soup_child2 = str(soup_child).replace(str(tags_index), str(i))
                soup_child2 = BeautifulSoup(soup_child2, 'lxml-xml')
                new_group.append(soup_child2)
                array.insert_after(new_group)

        text = array.find_all('Text')
        for i in range(tags_count):
            for t in range(len(text)):
                soup_child_t = BeautifulSoup(str(text[t]), 'lxml-xml')
                # new_group_t = soup_child_t.new_tag('Group')
                soup_child_t2 = str(soup_child_t).replace(str(tags_index), str(i))
                soup_child_t2 = BeautifulSoup(soup_child_t2, 'lxml-xml')
                # new_group_t.append(soup_child_t2)
                array.insert_after(soup_child_t2)

        image = array.find_all('Image')
        for i in range(tags_count):
            for t in range(len(image)):
                soup_child_i = BeautifulSoup(str(image[t]), 'lxml-xml')
                # new_group_i = soup_child_i.new_tag('Group')
                soup_child_i2 = str(soup_child_i).replace(str(tags_index), str(i))
                soup_child_i2 = BeautifulSoup(soup_child_i2, 'lxml-xml')
                # new_group_i.append(soup_child_i2)
                array.insert_after(soup_child_i2)

        variable = array.find_all('Var')
        for i in range(tags_count):
            for t in range(len(variable)):
                soup_child_v = BeautifulSoup(str(variable[t]), 'lxml-xml')
                # new_group_v = soup_child_v.new_tag('Group')
                soup_child_v2 = str(soup_child_v).replace(str(tags_index), str(i))
                soup_child_v2 = BeautifulSoup(soup_child_v2, 'lxml-xml')
                # new_group_v.append(soup_child_v2)
                array.insert_after(soup_child_v2)

        array.extract()

    # print(soup)
    return soup
    # return soup.prettify(indent_width=4)


def eval_decimal(code):
    code = str(code).replace('{', '').replace('}', '')
    try:
        # print(10086, code)
        if isinstance(eval(code), float):
            decimal_value = Decimal(eval(code))
            evaluated_value = float(decimal_value.quantize(Decimal('0.00000001'), rounding=ROUND_DOWN))
            # print('eval_decimal', str(evaluated_value))
            return str(evaluated_value)
        else:
            return eval(code)
    except Exception as e:
        return code


def eval_safe(code, soup):
    if '[' in str(code) or ']' in str(code):
        # print('code: ', code)
        return get_array_num(code, soup)
    else:
        try:
            return eval_decimal(code)
        except Exception as e:
            if '{' in str(code) or '}' in str(code):
                return eval_safe(str(code).translate({ord(c): None for c in '{}'}), soup)
            else:
                return str(code).translate({ord(c): None for c in '{}'})

# def eval_safe(code, soup):
#     if '[' in str(code) or ']' in str(code):
#         return get_array_num(code, soup)
#     else:
#         try:
#             return eval(code)
#         except Exception as e:
#             return str(code).translate({ord(c): None for c in '{}'})
#             # print(e)
#             # pass


def eval_soup(soup, c_array_mode=0):

    # global_dict = {}
    global var_dict

    def get_var_dict(soup):

        # 循环查找变量
        def get_var_exp(var_expression, var_pre='#', soup=soup):
            if var_pre in var_expression:
                # print(var_expression, 110110)

                var_pre = '#'
                pattern = fr'{var_pre}\w+\b'
                re_var = re.search(pattern, str(var_expression))
                if re_var:
                    re_var_name = re_var.group()
                    re_var_tag = soup.find('Var', {'name': str(re_var_name[1:])})
                    if re_var_tag:
                        re_var_value = re_var_tag.get('expression', var_exp_default)
                        # print(f'\t {re_var_name}: {re_var_value}')
                        if var_pre in re_var_value:
                            re_var_value = get_var_exp(re_var_value, var_pre, soup)
                    else:
                        re_var_value = var_exp_default
                    return var_expression.replace(re_var_name, re_var_value)
            else:
                return var_expression

        global var_dict

        xml_string = str(soup).split('\n', 1)[1]
        xml_variable = get_xml_variable(str(xml_string))
        xml_variable = list(set(xml_variable))
        print('\t xml_variable:', xml_variable)

        var_dict = {}
        var_pre = ''

        for var_name in xml_variable:
            var_expression = ''
            for var in soup.find_all('Var', {"name": var_name}):

                if var.get('type') != 'string' and var.get('type') != 'number' and var.get('type') is not None\
                        or var.VariableAnimation is not None:
                    pass
                else:
                    var_pre = '@' if var.get('type') == 'string' else '#'
                    var_exp_default = '' if var_pre == '@' else '0'
                    var_expression = var.get('expression', var_exp_default)
                    var_expression = get_var_exp(var_expression)
                    # print(var_expression)
                    var_name = var_pre + var['name']
                    var_dict[var_name] = eval_decimal(var_expression)
                    # print(var_dict)
                    # breakpoint()

        return var_dict

    def do_loop_replace(soup, c_array_mode=0):

        pattern = r'\{([^}]+)\}'

        # 遍历所有标签
        # print('Loop Replace: ')
        for tag in soup.find_all():
            # 遍历标签的属性
            for attr, value in tag.attrs.items():
                # 判断属性值中是否包含正则匹配的格式
                if re.search(pattern, value):
                    # 获取匹配的内容
                    match = re.search(pattern, value)
                    expression = match.group(1)
                    if not c_array_mode:
                        for var, exp in var_dict.items():
                            expression = expression.replace(str(var), str(exp))
                    # 解析表达式并计算结果
                    evaluated_value = eval_safe(expression, soup)
                    # 在属性值中进行替换
                    if evaluated_value is not None:
                        if isinstance(evaluated_value, float):
                            decimal_value = Decimal(evaluated_value)
                            evaluated_value = float(decimal_value.quantize(Decimal('0.00000001'), rounding=ROUND_DOWN))

                        # 在属性值中进行替换
                        tag[attr] = tag[attr].replace(match.group(), str(evaluated_value))
                        for var, exp in var_dict.items():

                            tag[attr] = eval_decimal(str(tag[attr]).replace(str(var), str(exp)).replace('{', '').replace('}', ''))
                            if len(expression) >= 10 and __name__ == '__main__':
                                print('\t', expression, '=>', evaluated_value)

        if any(char in str(soup) for char in ['{', '}']):
            soup = do_loop_replace(soup)

        return soup

    global var_dict
    var_dict = get_var_dict(soup)

    if any(char in str(soup) for char in ['{', '}']):
        soup = do_loop_replace(soup, c_array_mode)

    # def evaluate_expression(var_dict):
    #
    #     evaluated_dict = {}
    #
    #     for key, value in var_dict.items():
    #         for var_key, var_value in var_dict.items():
    #             if var_key in value or 1:
    #                 value = value.replace(var_key, var_value)
    #
    #         evaluated_dict[key] = str(eval_decimal(value))
    #
    #     return evaluated_dict

    # for i in range(len(var_dict)):
    #     var_dict = evaluate_expression(var_dict)

    # 去除带有 '#' 的键值对
    new_var_dict = {}
    for key, value in var_dict.items():
        if '#' not in str(value):
            new_var_dict[key] = value
    var_dict = new_var_dict

    print('\t var_dict:', var_dict)

    return soup, var_dict


def get_array_num(var_parse, soup):
    # 提取变量名和索引
    var_parse = var_parse[1:]
    var_name, index_str = var_parse.split("[")
    index = eval_safe(index_str.rstrip("]"), soup)

    # 找到对应变量节点
    var_node = soup.find('Var', {'name': var_name})

    if var_node is not None:
        # 获取变量值
        values = var_node['values']
        value_list = [str(x.strip()).replace("'", "") for x in values.split(",")]

        # 根据索引获取值
        if index < len(value_list):
            value = value_list[index]
            return value
        else:
            print(f"Index {index} out of range")
    else:
        print(f"Variable {var_name} not found")


def c_array(code):
    soup = BeautifulSoup(code, 'lxml-xml')
    for array in soup.find_all('C_Array'):

        # arrays = array.contents
        # c_arrays = [item for item in arrays if item != '\n']
        # print(c_arrays)
        # if str(c_arrays[0]).startswith('<VariableCommand') and len(c_arrays) == 1:
        #     tag_list = ['VariableCommand']
        # else:
        #     tag_list = ['Button', 'Text', 'Image', 'Var']

        tag_list = ['Button', 'Text', 'Image', 'Var']

        # 改为自动化识别支持的标签
        for tags in array.find_all():
            if tags.parent.name == 'C_Array':
                # print(tags.name)
                tag_list.append(tags.name)
        tag_list = list(set(tag_list))
        # print(tag_list)

        # 搜索替换 【#_i】 为 count 循环后的数字
        tags_index = str('#' + array.get('indexName'))

        if array.get('count') is not None:
            tags_count = int(array.get('count'))

            text = array.find_all(lambda tag: tag.name in tag_list)

            reversed_add_mode = bool(array.get('reversed'))
            if reversed_add_mode:
                range_i = range(tags_count - 1, -1, -1)
            else:
                range_i = range(tags_count)

            for i in range_i:
                for t in range(len(text)):
                    soup_child_t = BeautifulSoup(str(text[t]), 'lxml-xml')
                    if soup_child_t and '[]' not in str(soup_child_t.get('type')):
                        # new_group_t = soup_child_t.new_tag('Group')
                        soup_child_t2 = str(soup_child_t).replace(str(tags_index), str(i))
                        soup_child_t2 = BeautifulSoup(soup_child_t2, 'lxml-xml')
                        # new_group_t.append(soup_child_t2)
                        array.insert_after(soup_child_t2)

            array.extract()

        elif (array.get('begin') is not None and array.get('end') is not None) or array.get('count') is None:

            array_begin = array.get('begin', "0")
            array_end = array.get('end', "1")

            begin = max(eval(array_begin), 0)
            end = max(eval(array_end) + 1, 1)
            # print(array.get('begin'), array.get('end'))

            text = array.find_all(lambda tag: tag.name in tag_list)

            for i in range(begin, end):
                for t in range(len(text)):
                    soup_child_t = BeautifulSoup(str(text[t]), 'lxml-xml')
                    if soup_child_t and '[]' not in str(soup_child_t.get('type')):
                        # new_group_t = soup_child_t.new_tag('Group')
                        soup_child_t2 = str(soup_child_t).replace(str(tags_index), str(i))
                        soup_child_t2 = BeautifulSoup(soup_child_t2, 'lxml-xml')
                        # new_group_t.append(soup_child_t2)
                        array.insert_after(soup_child_t2)

            array.extract()

        has_var_array = bool('[]' in str(soup))
        if has_var_array is True:
            soup = eval_soup(soup, 1)[0]
        else:
            pattern = r'\{([^}]+)\}'
            # 遍历所有标签
            for tag in soup.find_all():
                # 遍历标签的属性
                for attr, value in tag.attrs.items():
                    # 判断属性值中是否包含正则匹配的格式
                    if re.search(pattern, value):
                        # 获取匹配的内容
                        match = re.search(pattern, value)
                        expression = match.group(1)
                        # 解析表达式并计算结果
                        evaluated_value = eval(expression)
                        # 在属性值中进行替换
                        tag[attr] = tag[attr].replace(match.group(), str(evaluated_value))

        for empty_tag in soup.find_all():
            if empty_tag.get('visibility') == '0' or\
                    ('[]' in str(empty_tag.get('type')) and empty_tag.get('_c')) \
                    or ('0*eq' == str(empty_tag.get('visibility'))[0:4]) \
                    or ('eq(0,1)*' in str(empty_tag.get('visibility'))) \
                    or ('eq(0,2)*' in str(empty_tag.get('visibility'))) \
                    or ('eq(1,0)*' in str(empty_tag.get('visibility'))) \
                    or ('eq(1,2)*' in str(empty_tag.get('visibility'))) \
                    or ('eq(2,0)*' in str(empty_tag.get('visibility'))) \
                    or ('eq(2,1)*' in str(empty_tag.get('visibility'))):
                empty_tag.extract()

    if __name__ == '__main__':
        print(soup.prettify(indent_width=4))
    return soup


if __name__ == '__main__':
    a = 1
    b = 'DEBUGGER'
    # eval_content = 'eq(a,1)'
    # eval_content = 'substr(b,0,len(b))'
    # print(eval_safe(eval_content, ''))
    c_array(xml_content)
    # print(c_array(xml_content))
