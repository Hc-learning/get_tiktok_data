import os.path

from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from config.settings import SETTINGS_DATA
from selenium.webdriver.edge.service import Service

option = Options()
os.path.exists(SETTINGS_DATA.get('USER_FILE_PATH')) or os.mkdir(SETTINGS_DATA.get('USER_FILE_PATH'))

# # 爬虫反屏蔽
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
wd = webdriver.Edge(options=option)
wd.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get:()=>undefined})'
})
# 创建文件夹
# 设置浏览器数据存储路径
option.add_argument(f'--user-data-dir={SETTINGS_DATA.get("USER_FILE_PATH")}')
# 无头模式
# option.add_argument("--headless=old")
option.add_argument("--disable-gpu")
# option.add_argument('--headless')
driver = webdriver.Edge(service=Service(SETTINGS_DATA.get('edge_driver_path')), options=option)

# driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
#     'source': 'Object.defineProperty(navigator, "webdriver", {get:()=>undefined})'
# })

wait = WebDriverWait(driver, SETTINGS_DATA.get('Time_out'))

# input()