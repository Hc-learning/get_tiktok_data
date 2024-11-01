import logging
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from components.get_webdriver import driver, wait

# 通用的等待函数
def wait_for(_by,condition:str):
    try:
        wait.until(EC.presence_of_element_located((_by,condition)))
    except TimeoutException as e:
        logging.info(f"Timeout waiting for {_by} {condition}: {e}")
    except Exception as e:
        logging.info(f"Error waiting for {_by} {condition}: {e}")