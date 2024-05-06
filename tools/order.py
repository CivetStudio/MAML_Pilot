import pyperclip
from lxml import etree as ET


def orderXML(input_file, output_file=None, xml_minify=0):

    # import xml.etree.ElementTree as ET
    import xml.dom.minidom

    # import html
    #
    # def encodeChinese(text):
    #     # 使用 html.escape 将中文转换为 ASCII 编码
    #     encoded_text = html.escape(text, quote=True)
    #     return encoded_text

    # 读取 XML 文件
    tree = ET.parse(input_file)
    root = tree.getroot()

    # 定义新的属性顺序
    new_attribute_order = ["name", "type", "rate", "extra", "count", "index", "indexName", "expression", "values",
                           "threshold", "const", "persist",
                           "target", "targetIndex", "command", "method", "paramTypes", "params",
                           "easeType", "varSpeedFlag", "easeTime",
                           "sound", "volume", "keepCur", "property",
                           "value", "time", "dtime", "tag", "initPause", "loop", "numPara", "strPara",
                           "delay", "delayCondition", "condition",
                           "action", "actionExp", "uri", "uriExp",
                           "uriFormat", "uriParas", "columns", "where", "whereExp", "whereFormat", "whereParas", "args",
                           "order", "countName", "column", "row", "dependency",
                           "category", "package", "packageExp", "class", "classExp", "broadcast",
                           "x", "y", "align", "alignV", "width", "height", "w", "h", "color", "fillColor", "strokeColor",
                           "weight", "strokeAlign", "cap", "dash", "cornerRadius", "cornerRadiusExp",
                           "src", "srcid", "srcExp", "srcFormat", "srcFormatExp", "srcParas", "number", "string",
                           "space", "charNameMap", "antiAlias",
                           "haptic", "interceptTouch", "alignChildren",
                           "autoShow", "defAlbumCover", "enableLyric", "updateLyricInterval",
                           "size", "format", "formatExp", "paras", "text", "textExp", "bold",
                           "pivotX", "pivotY", "rotation", "rotationX", "rotationY", "rotationZ",
                           "centerX", "centerY", "angle", "angleX", "angleY", "angleZ", "scale", "scaleX", "scaleY",
                           "marqueeSpeed", "marqueeGap", "multiLine", "spacingMult", "spacingAdd",
                           "shadow", "shadowDx", "shadowDy", "shadowRadius", "Radius", "shadowColor",
                           "maxHeight", "data",
                           "blur", "alpha", "layered", "clip", "typeface", "fontFamily", "fontPath", "visibility",
                           "tint", "tintmode", "xfermode", "xfermodeNum",
                           "enableMove", "moveRect", "active",
                           "disabled", "alias", "_port"]

    # 遍历每个元素并重新排列属性
    for element in root.iter():
        if element.attrib:
            # 创建一个新属性字典，包含所有原始属性
            new_attributes = {key: element.attrib[key] for key in element.attrib}
            # 清空元素的属性
            element.attrib.clear()
            # 重新添加原始属性，按新顺序排列
            for attr_name in new_attribute_order:
                if attr_name in new_attributes:
                    element.attrib[attr_name] = new_attributes[attr_name]
            # 添加剩余的属性，不在新顺序列表中的属性也会被保留
            for attr_name, attr_value in new_attributes.items():
                if attr_name not in new_attribute_order:
                    element.attrib[attr_name] = attr_value

    # # 遍历每个元素并重新排列属性
    # for element in root.iter():
    #     if element.attrib:
    #         # 创建一个新属性字典，包含所有原始属性
    #         new_attributes = {key: element.attrib[key] for key in element.attrib}
    #         # 清空元素的属性
    #         element.attrib.clear()
    #         # 重新添加原始属性，按新顺序排列，并将中文字符编码为 ASCII
    #         for attr_name in new_attribute_order:
    #             if attr_name in new_attributes:
    #                 encoded_value = encodeChinese(new_attributes[attr_name])
    #                 element.attrib[attr_name] = encoded_value
    #         # 添加剩余的属性，不在新顺序列表中的属性也会被保留，并将中文字符编码为 ASCII
    #         for attr_name, attr_value in new_attributes.items():
    #             if attr_name not in new_attribute_order:
    #                 encoded_value = encodeChinese(attr_value)
    #                 element.attrib[attr_name] = encoded_value

    xml_str_modified = ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')

    if 'Welcome' not in xml_str_modified:
        # 创建两条注释
        comment1 = ET.Comment("欢迎定制锁屏：灵貓 QQ 1876461209  /  Welcome to customize the lock screen: Civet QQ 1876461209")
        comment2 = ET.Comment("违规抄袭将依据《中华人民共和国民法典》追究法律责任  /  Illegal plagiarism will be investigated for legal liability in accordance with the Civil Code of the People's Republic of China.")

        # 在根元素下添加注释
        root.insert(0, comment1)
        root.insert(1, comment2)

    # 将 XML 树输出为字符串
    xml_str_modified = '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(root, encoding='utf-8', xml_declaration=False).decode('utf-8')
    # print(xml_str_modified)

    # 使用xml.dom.minidom进行格式化
    formatted_xml = xml.dom.minidom.parseString(xml_str_modified).toprettyxml(indent="\t")

    if xml_minify:
        cleaned_xml_str = xml_str_modified
    else:
        # 去除额外的空行
        cleaned_xml_str = '\n'.join(line for line in formatted_xml.split('\n') if line.strip()) \
            .replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="utf-8"?>')

    # 保存到新文件
    if output_file is None:
        output_file = input_file

    # tree.write(output_file, encoding="utf-8", xml_declaration=True)
    # tree.write(output_file, encoding="ASCII", xml_declaration=True)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_xml_str)


if __name__ == "__main__":
    orderXML(pyperclip.paste())
