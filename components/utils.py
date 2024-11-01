import logging
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from components.get_webdriver import wait

# 通用的等待函数
def wait_for(_by,condition:str):
    try:
        wait.until(EC.presence_of_element_located((_by,condition)))
    except TimeoutException as e:
        logging.info(f"Timeout waiting for {_by} {condition}: {e}")
    except Exception as e:
        logging.info(f"Error waiting for {_by} {condition}: {e}")

# 獲取進度條
def progress_bar(prefix, statr_time, total, i, gd = 40, page_num = 1):
    if total >= gd:
        num = round((total * page_num) / gd)
        b = int((i / num))
        b = b if b <= gd else gd
        a = '█' * b + ('-' * (gd - b - 1))
        end_time = time.time()
        d = f'The time spent: {round(end_time - statr_time, 2)}/s'
        print(f'\r{prefix}:|{a}| [ {i}/{total} ] ( {d} )',end='')
    else:
        print(f'\r{prefix}: [ {i}/{total} ]',end='')