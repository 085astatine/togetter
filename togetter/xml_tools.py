# -*- coding: utf-8 -*-


import pathlib
from typing import Union
import lxml.etree


def save_as_xml(
            element_tree: Union[lxml.etree._Element, lxml.etree._ElementTree],
            filepath: Union[str, pathlib.Path],
            pretty_print: bool = True) -> None:
    """save ElementTree in the file as XML

    Args:
    element_tree (lxml.etree._ElementTree): the ElementTree to be save.
    filepath (str, pathlib.Path): The path of the File to be output as XML.
    pretty_print (bool) optional:
        The Argument of lxml.etree.tostring.
        Defaults to True.
    """
    if not isinstance(filepath, pathlib.Path):
        filepath = pathlib.Path(filepath)
    with filepath.open(mode='w', encoding='utf-8', newline='') as file:
        file.write(lxml.etree.tostring(
                    element_tree,
                    encoding='utf-8',
                    pretty_print=pretty_print,
                    xml_declaration=True).decode('utf-8'))
