import re
from bs4 import BeautifulSoup
orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


BeautifulSoup.prettify = prettify

xml_content = """
    
    <C_Array count="10" indexName="_i" >
    
        <Button x="10+#_i*10" y="10" w="100" h="100" visibility="1" >
            <Triggers>
                <Trigger action="up" >
                    <VariableCommand name="name_#_i" expression="5*#_i" type="number" />
                </Trigger>
            </Triggers>
        </Button>
        
        <Button x="500+#_i*500" y="600" w="900" h="900" visibility="300" >
            <Triggers>
                <Trigger action="up" >
                    <VariableCommand name="nnnnnn_#_i" expression="300*#_i" type="number" />
                </Trigger>
            </Triggers>
        </Button>
        
        <Text x="100+#Ani_#_i*300" y="100+#_i*100" color="#ff0000" size="50" text="Ani_#_i" />
        
    </C_Array>
    
"""


def c_array(code):
    soup = BeautifulSoup(code, 'lxml-xml')
    for array in soup.find_all('C_Array'):
        # 搜索替换 【#_i】 为 count 循环后的数字
        tags_index = str('#' + array.get('indexName'))
        tags_count = int(array.get('count'))
        tags = array.find_all('Button')
        for t in range(len(tags)):
            soup_child = BeautifulSoup(str(tags[t]), 'lxml-xml')
            new_group = soup_child.new_tag('Group')
            for i in range(tags_count):
                soup_child2 = str(soup_child).replace(str(tags_index), str(i))
                soup_child2 = BeautifulSoup(soup_child2, 'lxml-xml')
                new_group.append(soup_child2)
                array.insert_after(new_group)

        text = array.find_all('Text')
        for t in range(len(text)):
            soup_child_t = BeautifulSoup(str(text[t]), 'lxml-xml')
            new_group_t = soup_child_t.new_tag('Group')
            for i in range(tags_count):
                soup_child_t2 = str(soup_child_t).replace(str(tags_index), str(i))
                soup_child_t2 = BeautifulSoup(soup_child_t2, 'lxml-xml')
                new_group_t.append(soup_child_t2)
                array.insert_after(new_group_t)

        image = array.find_all('Image')
        for t in range(len(image)):
            soup_child_i = BeautifulSoup(str(image[t]), 'lxml-xml')
            new_group_i = soup_child_i.new_tag('Group')
            for i in range(tags_count):
                soup_child_i2 = str(soup_child_i).replace(str(tags_index), str(i))
                soup_child_i2 = BeautifulSoup(soup_child_i2, 'lxml-xml')
                new_group_i.append(soup_child_i2)
                array.insert_after(new_group_i)

        array.extract()

    return soup
    # return soup.prettify(indent_width=4)


if __name__ == '__main__':
    print(c_array(xml_content))
