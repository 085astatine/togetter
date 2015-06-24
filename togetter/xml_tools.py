# -*- coding: utf-8 -*-

import pathlib
import lxml.etree

def saveXML(element_tree, xml_path, pretty_print= True):
    if not isinstance(xml_path, pathlib.Path):
        xml_path = pathlib.Path(xml_path)
    with xml_path.open(mode= 'w', encoding= 'utf-8', newline= '') as file:
        file.write(lxml.etree.tostring(
                    element_tree,
                    encoding= 'utf-8',
                    pretty_print= pretty_print,
                    xml_declaration= True).decode('utf-8'))
