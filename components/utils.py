import logging
import time

import os
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from components.get_webdriver import wait

# 通用的等待函数
def wait_for(_by,condition:str):
    try:
        wait.until(EC.presence_of_element_located((_by,condition)))
    except TimeoutException as e:
        logging.info(f"Timeout waiting for {_by} {condition}: {e}")
        return False
    except Exception as e:
        logging.info(f"Error waiting for {_by} {condition}: {e}")
        return False
    return True

# 獲取進度條
def progress_bar(prefix,total, i):
    # if total >= gd:
    #     num = round((total * page_num) / gd)
    #     b = int((i / num))
    #     b = b if b <= gd else gd
    #     a = '█' * b + ('-' * (gd - b - 1))
    #     end_time = time.time()
    #     d = f'The time spent: {round(end_time - statr_time, 2)}/s'
    #     print(f'\r{prefix}:|{a}| [ {i}/{total} ] ( {d} )',end='')
    # else:
    print(f'\r{prefix}: [ {i}/{total} ]',end='')

# 拼圖驗證碼
def check_captcha():
    pass

# 保存數據與清理重複數據

def save_data(datas:list[dict],_page = None):
    # 判斷文件是否存在、
    df = pd.DataFrame(datas)
    if not os.path.exists('./data1.xlsx'):
        df.to_excel('./data1.xlsx',index=False)
    else:
        df_read = pd.read_excel('./data1.xlsx')
        df = pd.concat([df,df_read], ignore_index=True)
        df.to_excel('./data1.xlsx',index=False)
    logging.info(f'第[ {_page} ]輪數據保存完成')

def clear_data():
    df = pd.read_excel('./data1.xlsx')
    df = df.drop_duplicates(subset=['name'])
    df.to_excel('./data1.xlsx', index=False)
    return len(df)