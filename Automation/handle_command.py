import re
import time
import random
from hierarchy import *


def wait(duration=1):
    # Wait for the specified duration
    time.sleep(duration)


def restart(device, package_name):  
    device.app_stop(package_name) 
    time.sleep(2)
    device.app_start(package_name)
    time.sleep(2)

def scroll(device, index = 0, direction=None):
    if direction == 'up' or  direction == 'top' or direction == None:
        #device.swipe_ext("down", scale=0.8) 
        #device.swipe_ext("down", scale=0.8) 
        device(scrollable=True)[index].fling.vert.toBeginning()
    elif direction == 'down' or  direction == 'bottom':
        #device.swipe_ext("up", scale=0.8) 
        #device.swipe_ext("up", scale=0.8) 
        device(scrollable=True)[index].fling()
    elif direction == 'end':
        device(scrollable=True)[index].fling.toEnd()
    else:
        device.swipe_ext("down", scale=0.9) 


def orientation(device, command):
    direction = command.get('to_direction', None)
    if direction == None:
        direction = command.get('direction', None)
    if direction == None:   
        direction = command.get('orientation', None)
        
    if direction  == 'portrait':
        device.set_orientation('natural')
    elif direction == 'landscape':
        device.set_orientation('left')
    elif direction in ['left', 'right', 'natural', 'upsidedown']:
        device.set_orientation(direction)
    else:
        options = ['left', 'right', 'natural', 'upsidedown']
        current_orientation = device.orientation
        random_option = current_orientation
        while random_option == current_orientation:
            random_option = random.choice(options)

        device.set_orientation(random_option)

def swipe(device, direction=None):
    if direction == 'up':
        device.swipe_ext("up", scale=0.9) 
    elif direction == 'down':
        device.swipe_ext("down", scale=0.9) 
    elif direction == 'right':
        device.swipe_ext("right", scale=0.9) 
    else:

        device.swipe_ext("left", scale=0.9) 

def multiple_selection(device, items, attribute_to_element_map):
    
    if len(items) ==  0:
        return ("No items to select.")
    
    element = attribute_to_element_map.get(items[0], None)
    execute(device, element, {'feature':items[0], 'action':'long_click'})
    if len(items) > 1:
        for item in items[1:]:
            element = attribute_to_element_map.get(item, None)
            execute(device, element, {'feature':item, 'action':'click'})
    
def change_status(device, element, command):

    current_status = command.get('current_status', '')
    target_status = command.get('target_status', '')
    if current_status != target_status:
        return execute(device, element, command) 
def back(device):
    device.press('back')

def click(device, coor):
    device.click(coor[0],coor[1])
    return True

def long_click(device, coor):
    device.long_click(coor[0],coor[1], 1.5)
    return True

def set_text(device, rep_attr, input_text, index):
    ui_object = locate_ui_object(device, rep_attr, 'set_text', index)
    if ui_object is None:
        return False
    elif input_text == None:
        return 'Error: You did not provide the input_text for set_text'
    else:
        '''
        ui_object.set_text('1')
        time.sleep(1)
        try:
            ui_object.set_text(input_text)
        except:
            try:
                set_text(device, '1', input_text, index)
            except:
                return "fail locate the target"
        '''
        try:
            ui_object.set_text(input_text)
        except:
            return "fail locate the target"
        return True

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

def get_bounds_dict(bounds):
    pattern = r'^\[(\d+),(\d+)\]\[(\d+),(\d+)\]$'
    match = re.match(pattern, bounds)
    if not match:
        return None
    coordinates = [int(coord) for pair in bounds.split('][') for coord in pair.strip('[]').split(',')]

    if len(coordinates) != 4:
        raise ValueError(f"Expected 4 coordinates, but got {len(coordinates)}")

    bounds_dict = {'left': coordinates[0],
                'top': coordinates[1],
                'right': coordinates[2],
                'bottom': coordinates[3]}

    return bounds_dict


def locate_ui_object(device, rep_attr, type=None, index = 0):
    ui_object = device(text = rep_attr)[index]
    if ui_object:
        return ui_object
    
    ui_object = device(description = rep_attr)[index]
    if ui_object:
        return ui_object
    
    ui_object = device(resourceId = rep_attr)[index]
    if ui_object:
        return ui_object

    bounds_dict = get_bounds_dict(rep_attr)
    if bounds_dict is not None:
        for ui_object in device():
            if ui_object.info['bounds']==bounds_dict:
                if type == None:
                    return ui_object
                if type == 'set_text' and 'EditText' in ui_object.info['className']:
                    return ui_object


def get_element(attribute_to_element_map, command):
    if isinstance(command['feature'], dict):
        return None, f"command['feature'] is not the right format, please provide the feature only "

    element_list = attribute_to_element_map.get(command['feature'], [])
    if element_list != []:
        index = command.get('index', 0)
        if index >= len(element_list):
            return None, f"the idex, {index}, is out of range, {len(element_list)}"
        else:
            element = element_list[index]
    else:
        element = None
    return element, None

def execute(device, element, command):
    
    rep_attr = command['feature']
    action = command['action']
    index = command.get('index', 0)
        
    if action == 'set_text':
        
        return set_text(device, rep_attr, command.get('input_text', None), index)
        
    if action in ['click', 'long_click']:
        if element is None:
            if 'click' in action and index ==0:
                coor = get_center_if_coordinate(rep_attr)
                if coor:
                    globals()[action](device, coor)
                    return True
            ui_object = locate_ui_object(device, rep_attr, index)
            if ui_object:
                getattr(ui_object, action)()
                return True
        else:
            coor = get_center_if_coordinate(element.attrib.get('bounds', ''))
            if coor:
                globals()[action](device, coor)
                return True
    return False

def handle_command(command, device, attribute_to_element_map, package_name):
    command_map = {
        'complete': lambda: None,
        'restart': lambda: restart(device, package_name),
        'scroll': lambda: scroll(device, command.get('index', 0), command.get('to_direction', command.get('target_direction', None))),
        'orientation': lambda: orientation(device, command),
        'rotate': lambda: orientation(device, command),
        'back': lambda: back(device),
        'swipe': lambda: swipe(device, command.get('to_direction', None)),
        'multiple_selection': lambda: multiple_selection(device, command['features'], attribute_to_element_map),
        'Navigate up': lambda: back(device),
        'wait':lambda: wait(command.get('duration', None))
    }
    print(command)
    if command['action'] in command_map:
        command_map[command['action']]()
        return True
    elif command.get('feature', None) == None:
        return f"The program cannot regconized this actions {command}"
    elif command.get('current_status', '') and command.get('target_status', ''):
        element, warning = get_element(attribute_to_element_map, command)
        if warning is None:
            return change_status(device, element, command)
        else:
            return warning
    else:
        element, warning = get_element(attribute_to_element_map, command)
        if warning is None:
            return execute(device, element, command)
        else:
            return warning

   





