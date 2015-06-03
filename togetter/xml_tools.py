# -*- coding: utf-8 -*-

import pathlib
import xml.dom.minidom
import lxml.etree

def saveXML(element_tree, xml_path, pretty_print= True):
    if not isinstance(xml_path, pathlib.Path):
        xml_path = pathlib.Path(xml_path)
    with xml_path.open(mode= 'w', encoding= 'utf-8', newline= '') as file:
        # インデント整形された出力
        if pretty_print:
            temp_string = lxml.etree.tostring(
                        element_tree,
                        encoding= 'utf-8').decode('utf-8')
            reparsed = xml.dom.minidom.parseString(temp_string)
            file.write(reparsed.toprettyxml(
                        encoding= 'utf-8',
                        indent='    ').decode('utf-8'))
        # 単行での出力
        else:
            file.write(lxml.etree.tostring(
                        element_tree,
                        encoding= 'utf-8',
                        xml_declaration= True).decode('utf-8'))
