import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

driver = None
ActionChain = None
elements = {}
variables = {}

def findElement(element, index):
    return elements[element] if index is None else elements[element][int(index)]

def listOrNot(index):
    global elements
    if isinstance(elements[index], list) and len(elements[index]) == 1:
        elements[index] = elements[index][0]
    elif isinstance(elements[index], list) and len(elements[index]) == 0:
        raise KeyError ("No element with matching attributes found")

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def sleep(wait):
    time.sleep(int(wait))

def SET(typeVar, **kwargs):
    global variables
    for k, v in kwargs.items():
        if typeVar == 'float':
            variables[k] = float(v)
        elif typeVar == 'str':
            variables[k] = str(v)
        elif typeVar == 'int':
            variables[k] = int(v)
        else:
            raise AttributeError ("Given type is unsupported")
    print(variables)

def GET(variable):
    return variables[variable]

def EVALUATE(evaluation):
    print(evaluation)
    #evaluation = evaluation.replace(' ', '')
    #evaluation = evaluation.replace('get>', 'variables[')
    arreval = re.split('(\(|\)|\+|\-|\*|\/)', evaluation)
    for i, a in enumerate(arreval):
        print(arreval[i])
        arreval[i] = str(arreval[i]).replace('get>', "variables['")
        if arreval[i].startswith('variables'):
            arreval[i] = str(arreval[i])+"']"
            arreval[i] = eval(arreval[i], globals(), locals())
        for i, a in enumerate(arreval):
            try:
                arreval[i] = int(arreval[i])
            except:
                arreval[i] = arreval[i]
    return eval(''.join([str(a) for a in arreval]))

def start(browser, path='/'):
    global driver
    if browser.upper() == 'CHROME':
        driver = webdriver.Chrome(path)
    elif browser.upper() == 'FIREFOX':
        driver = webdriver.Firefox(path)
    elif browser.upper() == 'EDGE':
        driver = webdriver.Edge(path)
    elif browser.upper() == 'SAFARI':
        driver = webdriver.Safari(path)

def get_element_by_name(name, index):
    global elements
    elements[index] = driver.find_elements_by_name(name)
    listOrNot(index)

def get_element_by_class(class_name, index):
    global elements
    elements[index] = driver.find_elements_by_class_name(class_name)
    listOrNot(index)

def action_initialize():
    global ActionChain
    ActionChain = ActionChains(driver)

def text_action(*text_args, enter="True"):
    ActionChain.send_keys(*text_args)
    if str2bool(enter):
        ActionChain.send_keys(Keys.ENTER)

def action_perform():
    global ActionChain
    ActionChain.perform()

def get_element_by_id(elem_id, index):
    global elements
    elements[index] = driver.find_elements_by_id(elem_id)
    listOrNot(index)

def get_element_by_xpath(xpath, index):
    global elements
    elements[index] = driver.find_elements_by_xpath(xpath)
    listOrNot(index)

def get_element_by_css_selector(selector, index):
    global elements
    elements[index] = driver.find_element_by_css_selector(selector)
    listOrNot(index)

def get_element_by_tag(tag, index):
    global elements
    elements[index] = driver.find_elements_by_tag_name(tag)
    listOrNot(index)

def get_element_by_link_text(mode, text, index):
    global elements
    if mode.lower() == "absolute":
        elements[index] = driver.find_elements_by_link_text(text)
    elif mode.lower() == "partial":
        elements[index] = driver.find_elements_by_partial_link_text(text)
    else:
        raise TypeError (f"undefined type {mode}")
    listOrNot(index)

def clear(element, index):
    findElement(element, index).clear()

def write(element, words, index=None, clear="True", enter="True"):
    if str2bool(clear):
        findElement(element, index).clear()
    findElement(element, index).send_keys(words)
    if str2bool(enter):
        findElement(element, index).send_keys(Keys.RETURN)

def click(element, index=None):
    findElement(element, index).click()

def switch_to(window_name):
    driver.switch_to_window(window_name)

def visit(*args):
    driver.get(*args)

def close():
    driver.close()

exec((open("extensions.py").read()), globals(), locals())
