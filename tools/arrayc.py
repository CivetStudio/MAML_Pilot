import re
from bs4 import BeautifulSoup

orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


BeautifulSoup.prettify = prettify

xml_content = """
<MAML>
    
    <C_Array count="1" indexName="_i" >
        
        <Button x="50" y="100+106*#_i" w="400" h="100" visibility="1">
            <Triggers>
                <Trigger action="click">
                    <VariableCommand persist="true" name="id_#_i" expression="not(#id_#_i)" type="number" />
                </Trigger>
            </Triggers>
        </Button>
        
        <Button x="500+#_i*500" y="600" w="900" h="900" visibility="300" >
            <Triggers>
                <Trigger action="up" >
                    <VariableCommand name="nnn_#_i" expression="300*#_i" type="number" />
                </Trigger>
            </Triggers>
        </Button>

    </C_Array>
    
    <C_Array begin="0" end="1" indexName="_j" >
        
        <Text x="13+#Ani_#_j*13" y="13+#_j*13" color="#ff0000" size="13" text="Ani_#_j" />
        <VariableCommand name="test_#index" expression="#index" type="number" />

    </C_Array>
    
    <!--
        <C_Array count="4" indexName="index">
        </C_Array>
    -->
    
</MAML>
    
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
                range_i = range(tags_count-1, -1, -1)
            else:
                range_i = range(tags_count)

            for i in range_i:
                for t in range(len(text)):
                    soup_child_t = BeautifulSoup(str(text[t]), 'lxml-xml')
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
                    # new_group_t = soup_child_t.new_tag('Group')
                    soup_child_t2 = str(soup_child_t).replace(str(tags_index), str(i))
                    soup_child_t2 = BeautifulSoup(soup_child_t2, 'lxml-xml')
                    # new_group_t.append(soup_child_t2)
                    array.insert_after(soup_child_t2)

            array.extract()

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

    if __name__ == '__main__':
        print(soup.prettify(indent_width=4))
    return soup


if __name__ == '__main__':
    c_array(xml_content)
    # print(c_array(xml_content))
