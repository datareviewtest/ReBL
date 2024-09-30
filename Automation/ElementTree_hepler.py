
import xml.etree.ElementTree as ET

def build_children_map(element):
    return {parent: list(parent) for parent in element.iter()}

def build_parent_map(tree):
    return {c: p for p in tree.iter() for c in p}

def get_descendants(element):
    return [child for child in element] + [descendant for child in element for descendant in get_descendants(child)]

def get_siblings(element, parent_map):
    parent = parent_map.get(element)
    if parent:
        return [child for child in parent if child != element]
    else:
        return []


def all_children_are_leaves(element):
   
    for child in element:
        if len(list(child)) > 0:
            return False
    return True

def is_clickable_or_has_clickable_children(node):
    if node.attrib.get('clickable', '') == "true":
        return True
    for child in node:
        if child.attrib.get('clickable', '') == "true":
            return True
    return False

def check_error_keywords(tree, package_name):
    keywords = ['error', 'has stopped', 'crash', 'has crashed']
    for element in tree.iter():
        if element.attrib.get('package', '') != package_name:
            error_text = element.attrib.get('text', '').lower()  
            if any(keyword in error_text for keyword in keywords):
                return True
    return False

def get_system_text(tree, package_name):
    system_text = []
    for element in tree.iter():
        if element.attrib.get('package', '') != package_name:
            text = element.attrib.get('text', '').lower()  
            system_text.append(text)
    return False

def get_rep_attr(element, black_list=[]):

    if element is None:
        return None

    text = element.attrib.get('text', '')
    content_desc = element.attrib.get('content-desc', '')
    resource_id = element.attrib.get('resource-id', '')
    bounds = element.attrib.get('bounds', '')
    
    if content_desc:
        return content_desc    
    elif 'button' in resource_id and text:
        return text
    elif resource_id and resource_id not in black_list:
        return resource_id
    elif text:
        if len(text) < 100:
            return text
        else:
            return bounds
    else:
        return bounds