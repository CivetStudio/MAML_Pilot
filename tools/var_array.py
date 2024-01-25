from bs4 import BeautifulSoup
import pyperclip


def main(strings):
    # strings = "<Var name=\"monthStr\" values=\"'一','二','三','四','五','六','七','八','九','十','十一','十二'\" expression=\"''\" type=\"string[]\" />"
    soup = BeautifulSoup(strings, features="lxml-xml")
    for var in soup.find_all('Var'):
        if var.get('values'):
            values = eval('[' + var.get('values') + ']')
        # print(arr_n)
        var_name = var.get('name')
        var_type = var.get('type')[:-2]
        var_index = var.get('index', '#mGamePos.index')

        # 创建根节点 <VarArray type="string">
        var_array = soup.new_tag('VarArray', type=var_type)

        # 创建 <Vars> 子节点
        vars_tag = soup.new_tag('Vars')

        # 创建 <Var name="TG" index="#mTiangan" /> 子节点
        var_tag = soup.new_tag('Var')
        var_tag['name'] = var_name
        var_tag['index'] = var_index
        vars_tag.append(var_tag)

        # 将 <Vars> 添加到 <VarArray>
        var_array.append(vars_tag)

        # 创建 <Items> 子节点
        items_tag = soup.new_tag('Items')

        # 创建 <Item> 子节点并添加到 <Items>
        for value in values:
            item_tag = soup.new_tag('Item', value=value)
            items_tag.append(item_tag)

        # 将 <Items> 添加到 <VarArray>
        var_array.append(items_tag)

        # 将 <VarArray> 添加到 BeautifulSoup 对象
        soup.append(var_array)

        return var_array.prettify()


_paste = pyperclip.paste().split('\n')
text_to_copy = ''

for i in range(len(_paste)):
    # print(_paste[i])
    if str(_paste[i]).strip() != '':
        print('\t')
        print(f'{i}:\n {main(_paste[i])}')
        text_to_copy = str(text_to_copy) + '\n\t' + str(main(_paste[i]))
        # 将文本复制到剪贴板
        pyperclip.copy(text_to_copy)
