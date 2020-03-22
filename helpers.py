import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class HelpCycle:
    def __init__(self):
        self.driver = None
        self.ActionChain = None
        self.elements = {}
        self.variables = {}

    def findElement(self, element, index):
        return self.elements[element] if index is None else self.elements[element][int(index)]

    def listOrNot(self, index):
        if isinstance(self.elements[index], list) and len(self.elements[index]) == 1:
            self.elements[index] = self.elements[index][0]
        elif isinstance(self.elements[index], list) and len(self.elements[index]) == 0:
            raise KeyError ("No element with matching attributes found")

    def str2bool(self, v):
      return v.lower() in ("yes", "true", "t", "1")

    def sleep(self, wait):
        time.sleep(int(wait))

    def SET(self, typeVar, **kwargs):
        for k, v in kwargs.items():
            if typeVar == 'float':
                self.variables[k] = float(v)
            elif typeVar == 'str':
                self.variables[k] = str(v)
            elif typeVar == 'int':
                self.variables[k] = int(v)
            else:
                raise AttributeError ("Given type is unsupported")
        print(self.variables)

    def GET(self, variable):
        return self.variables[variable]

    def EVALUATE(self, evaluation):
        print(evaluation)
        #evaluation = evaluation.replace(' ', '')
        #evaluation = evaluation.replace('get>', 'self.variables[')
        arreval = re.split('(\(|\)|\+|\-|\*|\/)', evaluation)
        for i, a in enumerate(arreval):
            print(arreval[i])
            arreval[i] = str(arreval[i]).replace('get>', "self.variables['")
            if arreval[i].startswith('self.variables'):
                arreval[i] = str(arreval[i])+"']"
            for i, a in enumerate(arreval):
                try:
                    arreval[i] = float(arreval[i])
                except:
                    arreval[i] = arreval[i]
        return eval(''.join([str(a) for a in arreval]))

    def Print(self, *values):
        print(*values)

    def start(self, browser, path='/'):
        if browser.upper() == 'CHROME':
            self.driver = webdriver.Chrome(path)
        elif browser.upper() == 'FIREFOX':
            self.driver = webdriver.Firefox(path)
        elif browser.upper() == 'EDGE':
            self.driver = webdriver.Edge(path)
        elif browser.upper() == 'SAFARI':
            self.driver = webdriver.Safari(path)

    def get_element_by_name(self, name, index):
        self.elements[index] = self.driver.find_elements_by_name(name)
        self.listOrNot(index)

    def get_element_by_class(self, class_name, index):
        self.elements[index] = self.driver.find_elements_by_class_name(class_name)
        self.listOrNot(index)

    def action_initialize(self):
        self.ActionChain = ActionChains(self.driver)

    def text_action(self, *text_args, enter="True"):
        self.ActionChain.send_keys(*text_args)
        if self.str2bool(enter):
            self.ActionChain.send_keys(Keys.ENTER)

    def action_perform(self):
        self.ActionChain.perform()

    def get_element_by_id(self, elem_id, index):
        self.elements[index] = self.driver.find_elements_by_id(elem_id)
        self.listOrNot(index)

    def get_element_by_xpath(self, xpath, index):
        self.elements[index] = self.driver.find_elements_by_xpath(xpath)
        self.listOrNot(index)

    def get_element_by_css_selector(self, selector, index):
        self.elements[index] = self.driver.find_element_by_css_selector(selector)
        self.listOrNot(index)

    def get_element_by_tag(self, tag, index):
        self.elements[index] = self.driver.find_elements_by_tag_name(tag)
        self.listOrNot(index)

    def get_element_by_link_text(self, mode, text, index):
        if mode.lower() == "absolute":
            self.elements[index] = self.driver.find_elements_by_link_text(text)
        elif mode.lower() == "partial":
            self.elements[index] = self.driver.find_elements_by_partial_link_text(text)
        else:
            raise TypeError (f"undefined type {mode}")
        self.listOrNot(index)

    def clear(self, element, index):
        self.findElement(element, index).clear()

    def write(self, element, words, index=None, clear="True", enter="True"):
        if self.str2bool(clear):
            self.findElement(element, index).clear()
        self.findElement(element, index).send_keys(words)
        if self.str2bool(enter):
            self.findElement(element, index).send_keys(Keys.RETURN)

    def click(self, element, index=None):
        self.findElement(element, index).click()

    def switch_to(self, window_name):
        self.driver.switch_to_window(window_name)

    def visit(self, *args):
        self.driver.get(*args)

    def close(self):
        self.driver.close()
