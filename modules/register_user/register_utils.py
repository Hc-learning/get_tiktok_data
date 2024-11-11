import logging
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def input_or_click_element(driver: WebDriver, wait: WebDriverWait, condition: tuple[str, str], incident:str = None ,element:WebElement = None, choose:int = 1, input_value:str = None ) -> WebElement | int |list[WebElement]:
    # 点击元素
    if element is None:
        element = wait_element_visible(driver, wait,condition, choose)
    else:
        element = wait_element_visible(driver, wait,(condition[0], condition[1]), choose, element)
    if element == -1: return -1
    if choose == 1:
        if incident == 'click':
            element.click()
        elif incident == 'input':
            element.send_keys(input_value)
    return element

def wait_element_visible(driver: WebDriver, wait: WebDriverWait, condition: tuple[str, str], choose:int, element:WebElement = None ) -> WebElement|int|list[WebElement]:
    try:
        dv = driver if element is None else element
        if choose == 1:
            wait.until(EC.visibility_of_element_located(condition))
            return dv.find_element(condition[0], condition[1])
        if choose == 2:
            wait.until(EC.visibility_of_all_elements_located(condition))
            return dv.find_elements(condition[0], condition[1])
    except Exception as e:
            logging.info(f'错误信息：{e}')
            return -1