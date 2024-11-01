import os.path

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from config.settings import SETTINGS_DATA
from selenium.webdriver.chrome.service import Service

option = Options()
# 爬虫反屏蔽
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
# 创建文件夹
os.path.exists(SETTINGS_DATA.get('USER_FILE_PATH')) or os.mkdir(SETTINGS_DATA.get('USER_FILE_PATH'))
# 设置浏览器数据存储路径
option.add_argument(f'--user-data-dir={SETTINGS_DATA.get("USER_FILE_PATH")}')
# 禁止通知弹窗
prefs = {
    'profile.default_content_setting_values':
        {
            'notifications': 2
        }
}
option.add_experimental_option('prefs', prefs)
# 无头模式
# option.add_argument('--headless=old')
# driver = webdriver.Chrome( service=SETTINGS_DATA.get('chrome_driver_path'), options=option)
driver = webdriver.Chrome(service=Service(SETTINGS_DATA.get('chrome_driver_path')), options=option)

driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get:()=>undefined})'
})

wait = WebDriverWait(driver, SETTINGS_DATA.get('Time_out'))
