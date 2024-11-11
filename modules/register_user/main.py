import logging
import time
import multiprocessing
from selenium.webdriver.common.by import By
from tenacity import retry, stop_after_attempt,wait_fixed

from modules.register_user.register_user import BrowserApi
from modules.register_user.register_utils import input_or_click_element


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1), reraise=True)
def register_user(driver, wait) -> None:
    driver.get('https://www.tiktok.com/foryou')
    input_or_click_element(driver, wait, (By.CSS_SELECTOR, '#header-login-button'), 'click')
    input_or_click_element(driver, wait, (By.CSS_SELECTOR, '[data-e2e="bottom-sign-up"]'), 'click')
    input_or_click_element(driver, wait, (By.CSS_SELECTOR, '[data-e2e="channel-item"]'), 'click')
    time.sleep(3)
    divs = input_or_click_element(driver, wait, (By.CSS_SELECTOR, '[role="combobox"]'), choose=2)
    divs[1].click()
    input_or_click_element(driver, wait, (By.ID, 'Month-options-item-0'), 'click')
    divs[2].click()
    input_or_click_element(driver, wait, (By.ID, 'Day-options-item-0'), 'click')
    divs[3].click()
    input_or_click_element(driver, wait, (By.ID, 'Year-options-item-23'), 'click')
    input_or_click_element(driver, wait, (By.CSS_SELECTOR, '.ep888o80'), 'click')
    input_or_click_element(driver, wait, (By.CSS_SELECTOR, '[name="email"]'), 'input',
                           input_value='xiaoxie@woworldtech.com')
    input_or_click_element(driver, wait, (By.CSS_SELECTOR, '[type="password"]'), 'input',
                           input_value='abc123..')

# ,proxyType='socks5', proxyIp='107.172.163.27', proxyPort='6543', proxyUser='cguvswgd',
#                       proxyPassword='4kht7p1ek6jk'
def run():
    browser_api = BrowserApi()
    browser_id = browser_api.createBrowser('xxx')
    try:
        res = browser_api.openBrowser(browser_id)
        driver, wait = browser_api.CreateDriver(res)
        time.sleep(200)
        register_user(driver, wait)
    except Exception as e:
        logging.error(e)
    finally:
        browser_api.deleteBrowser(browser_id)


if __name__ == '__main__':
    process = [multiprocessing.Process(target=run) for i in range(4)]
    for p in process:
        p.start()
    for p in process:
        p.join()