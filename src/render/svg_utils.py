from lxml import etree
from typing import Any

def find_and_replace(root: etree.ElementBase, element_id: str, new_text: str):
    element = root.find(f".//*[@id='{element_id}']")
    if element is not None:
        element.text = new_text

def justify_format(root: etree.ElementBase, element_id: str, new_text: Any, length: int = 0):
    if isinstance(new_text, int):
        new_text = f"{'{:,}'.format(new_text)}"
    new_text = str(new_text)
    find_and_replace(root, element_id, new_text)
    just_len = max(0, length - len(new_text))
    
    if just_len <= 2:
        dot_map = {0: '', 1: ' ', 2: '. '}
        dot_string = dot_map[just_len]
    else:
        dot_string = ' ' + ('.' * just_len) + ' '
    find_and_replace(root, f"{element_id}_dots", dot_string)
