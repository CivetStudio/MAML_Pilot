import os
import sys
import pyperclip
from lxml import etree
from xml.dom import minidom


def validate_xml_syntax(xml_string):
    global validate_xml_syntax

    try:
        # Parse the XML string
        minidom.parseString(xml_string)
        print("XML syntax is valid.")
        validate_xml_syntax = 1
    except Exception as e:
        print(f"Error: {e}")
        print("XML syntax is not valid.")
        validate_xml_syntax = 0


def validate_xml_with_xsd(xml_content, xsd_content):
    try:
        xmlschema = etree.XMLSchema(etree.fromstring(xsd_content))
        xml_doc = etree.fromstring(xml_content)
        xmlschema.assertValid(xml_doc)
        return True
    except etree.XMLSyntaxError as e:
        print(f"Error: Invalid XML - {e}")
        return False


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    xsd_filename = "manifest.xsd"
    # xsd_filename = "manifest_hw.xsd"
    xsd_path = os.path.join(script_dir, xsd_filename)

    # Read XSD content as bytes
    with open(xsd_path, 'rb') as xsd_file:
        xsd_content = xsd_file.read()

    try:
        # Read the XML content from the specified XML file path
        # maml_main_xml = input("Enter the path of the XML file: ")
        maml_main_xml = pyperclip.paste().replace('\\', '/').replace('"', '')

        maml_file_name = os.path.basename(maml_main_xml)
        maml_rule_file = '.xml'

        # 判断 maml_file_name 是否以 maml_rule_file 结尾
        if maml_rule_file not in maml_file_name:
            print(f"Error: File must be '{maml_rule_file}'")
            sys.exit(1)

        print('\t')
        print(f'Source: {maml_main_xml}\n')
        if not os.path.isfile(maml_main_xml):
            print("Error: XML file not found.")
            sys.exit(1)

        with open(maml_main_xml, 'rb') as xml_file:
            xml_content = xml_file.read()

        validate_xml_syntax(xml_content)

        if not validate_xml_syntax:

            if validate_xml_with_xsd(xml_content, xsd_content):
                print("✅Success: XML is valid according to the XSD.")
                # You can proceed with further processing or use the XML data here.
            else:
                print("Error: XML validation failed.")

    except (etree.XMLSyntaxError, pyperclip.PyperclipException) as e:
        print("Error: Unable to read XML content or XSD content. Make sure the files exist and are valid.")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
