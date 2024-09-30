import uiautomator2 as u2
import xml.etree.ElementTree as ET
from collections import defaultdict
from ElementTree_hepler import *
import time



def get_current_hierarchy(device):
    with open('tmp', 'w') as file:
        file.write(device.dump_hierarchy())
    xmlp = ET.XMLParser(encoding="utf-8")
    tree = ET.parse('tmp', parser=xmlp)
    return tree

def get_container_type(current_type, className, ):

    if current_type != 'click':
        return current_type
    
    if '.Switch' in className:
        return 'switch_widget'
    elif 'Spinner' in className:
        return 'spinner'
    elif 'CheckBox' in className:
        return 'check_box'
    elif 'EditText' in className:
        return 'set_text'
    return 'click'

def process_group_general(root, parent_map, info, attr_to_elements):
    attr_to_group_elments = defaultdict(list)
    group, other_text, visited_elements = [], [], []
    type = 'click'
    #if 'toolbar' in root.attrib.get('resource-id', ''):
    #    type='toolbar'
    if root.attrib.get('scrollable', 'false') == 'true':
        type = 'scrollable'

    # Iterate over all nodes
    for element in root.iter():
        visited_elements.append(element)
        clickable = element.attrib.get('clickable', 'false') == 'true'
        enabled = element.attrib.get('enabled', 'false') == 'true'
        text = element.attrib.get('text', '')
        content_desc = element.attrib.get('content-desc', '')
        resource_id = element.attrib.get('resource-id', '')
        className = element.attrib.get('class', '')
        
        type = get_container_type(type, className)
        className = className[className.rfind('.')+1:]

        if type == 'set_text':
            if resource_id and text :
                group.insert(0, {className : resource_id})
                #if 'EditText' in className:
                #    group.insert(0, {className : resource_id})
                #else:
                #    group.insert(0,  resource_id)
                group.insert(0, text)
                attr_to_group_elments[resource_id].append(element)
            elif resource_id:
                 group.insert(0, {className : resource_id})
                #if 'EditTxt' in className:
                #    group.insert(0, {className : resource_id})
                #else:
                #    group.insert(0,  resource_id)
            elif text:
                group.insert(0, text)
                attr_to_group_elments[resource_id].append(element)
            else:
                bounds = element.attrib.get('bounds', '')
                group.insert(0, bounds)
                attr_to_group_elments[bounds].append(element)
        elif 'CheckBox' in className :
            if group != [] or other_text!=[]:
                group.append('status:checked' if element.attrib.get('checked', '') == 'true' else 'status:unchecked')
            elif text != '':
                group.extend( [text,  'status:checked' if element.attrib.get('checked', '') == 'true' else 'status:unchecked'])
                attr_to_group_elments[text].append(element)
            elif resource_id:
                group.extend([resource_id, 'status:checked' if element.attrib.get('checked', '') == 'true' else 'status:unchecked'])
                attr_to_group_elments[resource_id].append(element)
            else:
                bounds = element.attrib.get('bounds', '')
                group.extend([ bounds,  'status:checked' if element.attrib.get('checked', '') == 'true' else 'status:unchecked'])
                attr_to_group_elments[bounds].append(element)
        elif clickable:
                if content_desc:
                    if enabled:
                        group.insert(0, {className : content_desc})
                    else: 
                        group.insert(0, 'disabled')
                        group.insert(0, {className : content_desc})
                    attr_to_group_elments[content_desc].append(element)
            
                elif text:
                    group.insert(0, text)
                    attr_to_group_elments[text].append(element)
                    
                elif resource_id :
                    group.insert(0, {className : resource_id})
                    attr_to_group_elments[resource_id].append(element)
                
                elif element.attrib.get('NAF', '') == 'true':
                    bounds = element.attrib.get('bounds', '')
                    group.insert(0, {'NAF': bounds})
                    attr_to_group_elments[bounds].append(element)
        elif text and len(text)<50:
            
            other_text.append(text)
            attr_to_group_elments[text].append(element)

    if other_text:
        group.extend(other_text)
      

    
    info['visited'].extend(visited_elements)
    
    
    for key, value in attr_to_group_elments.items():
       if key in attr_to_elements:
           attr_to_elements[key].extend(value)
       else:
           attr_to_elements[key] = value
    root_id = root.attrib.get('resource-id', '') 
    if group != []:
        if root_id and root_id not in group:
            info[type].append(f"{root_id[root_id.rfind('/')+1:]}:{group}")

        else:
            info[type].append(f"{group}")

    

# Get elements that support operations like click, long click, and text input
#root, package_name, parent_map, info, attribute_to_element_map
def get_operable_elements(element, package_name, parent_map, info, attr_to_elements):
    
    if element.tag == 'node':
        #Filter out elements with package "com.android.systemui"
        if element.attrib.get('package', '') == 'com.android.systemui':
            return
        if element in info['visited']:
            return 
        clickable = element.attrib.get('clickable', 'false') == 'true'
        long_clickable = element.attrib.get('long-clickable', 'false') == 'true'
        text = element.attrib.get('text', '')
        content_desc = element.attrib.get('content-desc', '')
        resource_id = element.attrib.get('resource-id', '')
        #'edittext' in resource_id
        info['visited'].append(element)
        if 'toolbar' in resource_id:
            process_group_general(element, parent_map, info, attr_to_elements)
        elif (clickable or long_clickable) and not (text or content_desc or resource_id):
             process_group_general(element, parent_map, info, attr_to_elements)  
        elif all_children_are_leaves(element) and is_clickable_or_has_clickable_children(element): 
            process_group_general(element, parent_map, info, attr_to_elements)
        elif (clickable or long_clickable):
            if content_desc:
                info['click'].append([content_desc])

                #attr_to_elements[content_desc].append(element)
                if content_desc in attr_to_elements:
                    attr_to_elements[content_desc].append(element)
                else:
                    attr_to_elements.setdefault(content_desc, []).append(element)
            elif text and len(text) < 100:
                info['click'].append([text])
                attr_to_elements[text].append(element)
            elif resource_id:
                info['click'].append([resource_id])
                #attr_to_elements.setdefault(resource_id, []).append(element)
                if resource_id in attr_to_elements:
                    attr_to_elements[resource_id].append(element)
                else:
                    attr_to_elements.setdefault(resource_id, []).append(element)
        elif text != '':
            info['local_text'].append(text) 
        
    for child in element:
        get_operable_elements(child, package_name, parent_map, info, attr_to_elements)
    

def get_sequential_info(info, activity, orientation, toast):
    info['Other Widgets with Text in This Page'] = info["local_text"]
    del info["visited"]
    del info["local_text"]

    info = {k: v for k, v in info.items() if v != [] and v != [[]]}
   
    info_string = ''
    for key, values in info.items():
        info_string += f"{key} has the following group(s):"
        i = 1
        for v in values:
            info_string +=  f"{i}#.{v};" 
            i +=1
        #info_string +="\n"
    if toast is not None:
        return f"\n*Current Screen Information:  #Current Activity: {activity}. # UI Information:{info_string}.Toast message on the page: {toast}" 
    else:
        return f"\n*Current Screen Information:  #Current Activity: {activity}.  # UI Information:{info_string}."
    #return f"\n*Current Screen Information:  #Current Activity: {activity}.  # UI Information:{info_string}." 



def get_screen_information(device, attribute_to_element_map, package_name):
    try:
        toast = device.toast.get_message(2, 5, None)
    except:
        toast = None
    #toast = device.last_toast
    
    tree = get_current_hierarchy(device)
    root = tree.getroot()
    parent_map = build_parent_map(tree)
    info = {'toolbar':[], 'set_text':[], 'click':[], 'spinner':[], 'check_box':[], 'switch_widget':[], 'scrollable':[], 'local_text':[],'visited':[]}
   
    activity = device.app_current()['activity']
    get_operable_elements(root, package_name, parent_map, info, attribute_to_element_map)
  

    return info, get_sequential_info(info, activity, device.orientation, toast)

def print_screen_information_testing(emulator_id):

    device = u2.connect(emulator_id)
    package_name = device.app_current()['package']
    start_time = time.time()
    widget_dict, prompt = get_screen_information(device, {}, package_name)

    print(prompt)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")



