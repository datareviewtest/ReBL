
import re
import time
from uiautomator2 import Direction



def swipe(device, direction):
    if direction == 'up':
        device.swipe_ext("up", scale=0.9) 
    elif direction == 'down':
        device.swipe_ext("down", scale=0.9) 
    elif direction == 'left':
        device.swipe_ext("left", scale=0.9) 
    else:
     device.swipe_ext("right", scale=0.9) 
   

def restart(device, package_name):  
    device.app_stop(package_name) 
    time.sleep(2)
    device.app_start(package_name)
    time.sleep(2)


def click(device, coor):
    device.click(coor[0],coor[1])

def long_click(device, coor):
    device.long_click(coor[0],coor[1], 1.5)

def set_text(device, rep_attr, list):
    ui_object = locate_ui_object(device, rep_attr)
    if ui_object and len(list) > 2:
        ui_object.set_text(list[2])
    else:
        print("Warning: no suggested text", list)


def execute_suggestion(suggestion_list, attribute_to_element_map, device, package_name):
    for suggestion in suggestion_list:
        if suggestion[0] == 'complete':
            return
        elif suggestion[0] == 'restart':
            restart(device, package_name)
        elif suggestion[0] == 'scroll':
            device().fling()
        elif suggestion[0] == 'orientation':
            device.set_orientation('l')
        elif suggestion[0] == 'back':
            device.press('back')
        elif suggestion[0] == 'swipe':
            swipe(device, suggestion[1])
            print('execute swipe left')
        else:
            attribute = suggestion[0]
            element = attribute_to_element_map.get(attribute)
            execute(device, element, suggestion)
            time.sleep(3)


def get_center_if_coordinate(s):
    pattern = r'^\[(\d+),(\d+)\]\[(\d+),(\d+)\]$'
    match = re.match(pattern, s)
    if match:
        x1, y1, x2, y2 = map(int, match.groups())
        centerX = (x1 + x2) // 2
        centerY = (y1 + y2) // 2
        return [centerX, centerY]
    else:
        return None

def locate_ui_object(device, rep_attr):
    ui_object = device(text = rep_attr)
    if ui_object:
        return ui_object
    
    ui_object = device(description = rep_attr)
    if ui_object:
        return ui_object
    
    ui_object = device(resourceId = rep_attr)
    if ui_object:
        return ui_object


def execute(device, element, list):
    rep_attr = list[0]
    operation = list[1]
    
    if operation == 'set_text':
       set_text(device, rep_attr, list)
    elif element is None: 
        if len(list) == 3 and 'click' in list[2] and get_center_if_coordinate(list[0]):
            coor = get_center_if_coordinate(list[0])
            if operation == 'click':
                click(device, coor)
            elif operation == 'long_click':
                long_click(device, coor)
        ui_object = locate_ui_object(device, rep_attr)
        if ui_object:
            if operation == 'click':
                ui_object.click()
            elif operation == 'long_click':
                ui_object.long_click(1.5)
    else:
        operation = list[-1]
        coor = get_center_if_coordinate(element.attrib.get('bounds', ''))
        if coor and operation == 'click':
            click(device, coor)
        elif coor and operation == 'long_click':
            long_click(device, coor)
        else:
            print(operation, " is an invalid operation")

    

