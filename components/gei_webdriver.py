from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from config.settings import SETTINGS_DATA

option = Options()
# 爬虫反屏蔽
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
wd = webdriver.Edge(options=option)
wd.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get:()=>undefined})'
})

wait = WebDriverWait(wd, SETTINGS_DATA.get('Time_out'))
